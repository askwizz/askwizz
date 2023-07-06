from esearch.core.passage.definition import Passage


def get_passage_hash(passage: Passage) -> int:
    return hash(passage.text)
