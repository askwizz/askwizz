import hashlib


def encode_string(string: str) -> str:
    return hashlib.md5(string.encode("utf-8")).hexdigest()


def get_passage_hash(text: str) -> str:
    return encode_string(text)
