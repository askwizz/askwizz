import json
import logging
from collections import defaultdict
from typing import Annotated, Any, AsyncGenerator, List, Optional
from uuid import uuid4

from fastapi import Depends
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    Partition,
    SearchResult,
    connections,
    utility,
)

from esearch.api.authorization import UserData, get_current_user_dependency
from esearch.api.lifespan import ML_MODELS
from esearch.core.models.embeddings.e5 import CustomEmbeddings
from esearch.core.passage.definition import DocumentReference, Passage, PassageMetadata
from esearch.core.passage.format import get_json_from_passage_metadata
from esearch.services.milvus.entity import RetrievedPassage

DEFAULT_SEARCH_PARAMS = {
    "IVF_FLAT": {"metric_type": "L2", "params": {"nprobe": 10}},
    "IVF_SQ8": {"metric_type": "L2", "params": {"nprobe": 10}},
    "IVF_PQ": {"metric_type": "L2", "params": {"nprobe": 10}},
    "HNSW": {"metric_type": "L2", "params": {"ef": 10}},
    "RHNSW_FLAT": {"metric_type": "L2", "params": {"ef": 10}},
    "RHNSW_SQ": {"metric_type": "L2", "params": {"ef": 10}},
    "RHNSW_PQ": {"metric_type": "L2", "params": {"ef": 10}},
    "IVF_HNSW": {"metric_type": "L2", "params": {"nprobe": 10, "ef": 10}},
    "ANNOY": {"metric_type": "L2", "params": {"search_k": 10}},
    "AUTOINDEX": {"metric_type": "L2", "params": {}},
}


def get_passage_metadata_schema() -> List[FieldSchema]:
    return [
        FieldSchema("indexed_at", DataType.VARCHAR, max_length=256),
        FieldSchema("created_at", DataType.VARCHAR, max_length=256),
        FieldSchema("last_update", DataType.VARCHAR, max_length=256),
        FieldSchema("creator", DataType.VARCHAR, max_length=1024),
        FieldSchema("link", DataType.VARCHAR, max_length=1024),
        FieldSchema("document_link", DataType.VARCHAR, max_length=1024),
        FieldSchema("reference", DataType.VARCHAR, max_length=4096),
        FieldSchema("filetype", DataType.VARCHAR, max_length=128),
        FieldSchema("connection_id", DataType.VARCHAR, max_length=128),
        FieldSchema("indexor", DataType.VARCHAR, max_length=1024),
    ]


class Milvus:
    def __init__(
        self: "Milvus", user_id: str | None, embedder: CustomEmbeddings
    ) -> None:
        self.collection_name = user_id or ""
        self.connection_alias = uuid4().hex
        self.embedder = embedder
        self.host = "127.0.0.1"
        self.port = "19530"
        connections.connect(alias=self.connection_alias, host=self.host, port=self.port)
        self.consistency_level = "Session"
        self._primary_field = "pk"
        self._vector_field = "vector"

        self._get_collection()
        self._create_index()
        self._create_search_params()
        self._load_collection()

    def _get_collection_schema(self: "Milvus") -> CollectionSchema:
        fields = [
            FieldSchema(
                self._primary_field, DataType.INT64, is_primary=True, auto_id=True
            ),
            FieldSchema(
                self._vector_field,
                DataType.FLOAT_VECTOR,
                dim=self.embedder.embedding_size,
            ),
            *get_passage_metadata_schema(),
        ]
        return CollectionSchema(fields)

    def _get_index(self: "Milvus") -> Optional[dict[str, Any]]:
        """Return the vector index information if it exists"""

        if isinstance(self.collection, Collection):
            for x in self.collection.indexes:
                if x.field_name == self._vector_field:
                    return x.to_dict()
        return None

    def _create_index(self: "Milvus") -> None:
        if self._get_index() is not None:
            return
        self.collection.create_index(
            self._vector_field,
            index_params={
                "metric_type": "L2",
                "index_type": "HNSW",
                "params": {"M": 8, "efConstruction": 64},
            },
            using=self.connection_alias,
        )

    def _create_search_params(self: "Milvus") -> None:
        index = self._get_index()
        if index is None:
            return
        index_type: str = index["index_param"]["index_type"]
        metric_type: str = index["index_param"]["metric_type"]
        self.search_params = DEFAULT_SEARCH_PARAMS[index_type]
        self.search_params["metric_type"] = metric_type

    def _get_collection(self: "Milvus") -> None:
        has_connection = utility.has_collection(
            self.collection_name, using=self.connection_alias
        )
        new_schema = self._get_collection_schema()
        if has_connection:
            conn = connections._fetch_handler(self.connection_alias)
            resp = conn.describe_collection(self.collection_name)
            server_schema = CollectionSchema.construct_from_dict(resp)
            if server_schema != new_schema:
                old_connection = Collection(
                    self.collection_name,
                    schema=server_schema,
                    using=self.connection_alias,
                )
                old_connection.drop()
        self.collection = Collection(
            self.collection_name,
            schema=new_schema,
            using=self.connection_alias,
        )

    def _load_collection(self: "Milvus") -> None:
        self.collection.load()

    def close_connection(self: "Milvus") -> None:
        connections.disconnect(alias=self.connection_alias)

    def get_schema_fields(self: "Milvus", collection: Collection) -> List[str]:
        schema = collection.schema
        return [x.name for x in schema.fields if x.name != self._primary_field]

    def delete_partition(self: "Milvus", connection_key: str) -> None:
        partition = Partition(self.collection, connection_key)
        self.collection.release()
        partition.release()
        partition.drop()
        self._load_collection()

    def index_passages(
        self: "Milvus",
        embedder: CustomEmbeddings,
        passages: List[Passage],
        connection_key: str,
        is_first_batch: bool = False,
    ) -> None:
        if is_first_batch:
            if self.collection.has_partition(connection_key):
                self.delete_partition(connection_key)
            self.collection.create_partition(connection_key)

        passage_texts = [p.text for p in passages]
        debug = False
        if debug:
            with open("passage_texts.txt", "w") as f:
                for item in passage_texts:
                    f.write("%s\n" % item)

        try:
            embeddings = embedder.embed_documents(passage_texts)
        except NotImplementedError:
            embeddings = [embedder.embed_query(x) for x in passage_texts]

        if len(embeddings) == 0:
            logging.info("Nothing to insert, skipping.")
            return
        insert_dict = defaultdict(list)
        insert_dict[self._vector_field] = embeddings

        for passage in passages:
            for key, value in get_json_from_passage_metadata(passage.metadata).items():
                insert_dict[key].append(value)

        schema_fields = self.get_schema_fields(self.collection)
        insert_list = [insert_dict[field] for field in schema_fields]
        self.collection.insert(insert_list, timeout=None, partition_name=connection_key)

    def similarity_search(
        self: "Milvus",
        query: str,
        k: int = 4,
        param: Optional[dict] = None,
        **kwargs,  # noqa: ANN003
    ) -> List[RetrievedPassage]:
        embedding = self.embedder.embed_query(query)
        if self.collection is None:
            logging.debug("No existing collection to search.")
            return []

        param = self.search_params if param is None else param

        # Determine result metadata fields.
        output_fields = [
            x
            for x in self.get_schema_fields(self.collection)
            if x != self._vector_field
        ] + [self._primary_field]

        # Perform the search.
        search_result: SearchResult = self.collection.search(
            data=[embedding],
            anns_field=self._vector_field,
            param=param,
            limit=k,
            output_fields=output_fields,
            **kwargs,
        )  # type: ignore

        return [
            RetrievedPassage(
                score=result.score,
                metadata=PassageMetadata(
                    indexed_at=result.entity.get("indexed_at"),
                    created_at=result.entity.get("created_at"),
                    last_update=result.entity.get("last_update"),
                    creator=result.entity.get("creator"),
                    link=result.entity.get("link"),
                    document_link=result.entity.get("document_link"),
                    reference=DocumentReference(
                        **json.loads(result.entity.get("reference"))
                    ),
                    filetype=result.entity.get("filetype"),
                    connection_id=result.entity.get("connection_id"),
                    indexor=result.entity.get("indexor"),
                ),
                passage_id=result.entity.get(self._primary_field),
            )
            for result in search_result[0]
        ]


async def milvus_dependency(
    user: Annotated[UserData, Depends(get_current_user_dependency)]
) -> AsyncGenerator[Milvus, None]:
    milvus_client = Milvus(user.user_id, ML_MODELS["embedder"])
    try:
        yield milvus_client
    finally:
        milvus_client.close_connection()
