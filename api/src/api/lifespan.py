from contextlib import asynccontextmanager
from typing import Callable

from core.models.rwkv import LLMModel
from fastapi import FastAPI
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

from api.settings import AppSettings

ml_models = {}


def get_lifespan(app_settings: AppSettings) -> Callable[[FastAPI], None]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> None:  # noqa: ARG001
        # Load the ML model
        ml_models["llm"] = LLMModel.from_path(app_settings.rwkv_model_path)
        ml_models["embedder"] = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2",
            model_kwargs={"device": "cpu"},
        )
        yield
        # Clean up the ML models and release the resources
        ml_models.clear()

    return lifespan
