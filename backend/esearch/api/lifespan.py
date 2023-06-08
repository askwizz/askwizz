from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable

from esearch.core.models.embeddings import load_embedder
from esearch.core.models.rwkv import LLMModel
from fastapi import FastAPI

from esearch.api.settings import AppSettings

ml_models = {}


def get_lifespan(
    app_settings: AppSettings,
) -> Callable[[FastAPI], _AsyncGeneratorContextManager]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa: ARG001
        # Load the ML model
        ml_models["embedder"] = load_embedder(app_settings.embedder_model_name)
        ml_models["llm"] = LLMModel.from_path(app_settings.rwkv_model_path)
        yield
        # Clean up the ML models and release the resources
        ml_models.clear()

    return lifespan
