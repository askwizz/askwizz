from typing import Any

from langchain.embeddings.huggingface import HuggingFaceEmbeddings


class CustomHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    embedding_size: int = 768

    def __init__(
        self: "CustomHuggingFaceEmbeddings", **kwargs: Any  # noqa: ANN401
    ) -> None:
        super().__init__(
            **(
                kwargs
                | {
                    "model_name": "sentence-transformers/all-mpnet-base-v2",
                    "model_kwargs": {"device": "cpu"},
                }
            )
        )
