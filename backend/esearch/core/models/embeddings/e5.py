import logging
from typing import Any, List, Literal

import torch.nn.functional as func
from langchain.embeddings.base import Embeddings
from pydantic import BaseModel, Extra
from torch import Tensor
from tqdm import tqdm
from transformers import AutoModel, AutoTokenizer


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


class CustomEmbeddings(Embeddings):
    embedding_size: int


MODEL_SIZES = {
    "base": {
        "size": 768,
        "model": "intfloat/e5-base-v2",
    },
    "small": {
        "size": 384,
        "model": "intfloat/e5-small-v2",
    },
}

model_type = Literal["base"] | Literal["small"]


class E5v2(BaseModel, CustomEmbeddings):
    tokenizer: Any = None  #: :meta private:
    model: Any = None  #: :meta private:
    batch_size: int = 32
    embedding_size: int = 768

    def __init__(
        self: "E5v2", model: model_type = "base", **kwargs: Any  # noqa: ANN401
    ) -> None:
        super().__init__(**kwargs)
        self.embedding_size = MODEL_SIZES[model]["size"]
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_SIZES[model]["model"])
        self.model = AutoModel.from_pretrained(MODEL_SIZES[model]["model"])

    def _embed_texts(self: "E5v2", texts: List[str], prompt: str) -> List[List[float]]:
        texts_with_prompt = [prompt + t for t in texts]
        batch_dict = self.tokenizer(
            texts_with_prompt,
            max_length=512,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )
        outputs = self.model(**batch_dict)
        embeddings = average_pool(
            outputs.last_hidden_state, batch_dict["attention_mask"]  # type: ignore
        )
        embeddings = func.normalize(embeddings, p=2, dim=1)
        return embeddings.detach().numpy().tolist()

    def embed_documents(self: "E5v2", texts: List[str]) -> List[List[float]]:
        logging.info(f"Embedding {len(texts)} passages with E5Basev2...")
        all_embeddings = []
        for i in tqdm(range(0, len(texts), self.batch_size)):
            embeddings = self._embed_texts(texts[i : i + self.batch_size], "passage: ")
            all_embeddings.extend(embeddings)
        return all_embeddings

    def embed_query(self: "E5v2", text: str) -> List[float]:
        return self._embed_texts([text], "query: ")[0]

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
