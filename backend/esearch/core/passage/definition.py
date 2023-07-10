from enum import Enum

from pydantic import BaseModel


class ConfluenceDocumentReference(BaseModel):
    domain: str
    page_path: str
    chunk_id: str
    chunk_group: str
    start_index: int
    end_index: int
    space_key: str


class DocumentReference(BaseModel):
    text_hash: str
    confluence: ConfluenceDocumentReference | None = None


class DocumentType(Enum):
    CONFLUENCE = "CONFLUENCE"


class PassageMetadata(BaseModel):
    title: str
    indexed_at: str
    created_at: str
    last_update: str
    creator: str
    link: str
    document_link: str
    reference: DocumentReference
    filetype: DocumentType
    connection_id: str
    indexor: str


class Passage(BaseModel):
    text: str
    metadata: PassageMetadata
