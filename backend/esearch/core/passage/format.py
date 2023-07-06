import json

from esearch.core.passage.definition import PassageMetadata


def get_json_from_passage_metadata(metadata: PassageMetadata) -> dict:
    return {
        **metadata.dict(),
        "reference": json.dumps(metadata.reference.dict()),
        "filetype": metadata.filetype.value,
    }
