from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from typing import AsyncGenerator, Callable

from fastapi import FastAPI

from esearch.api.settings import AppSettings
from esearch.core.models.embeddings import load_embedder
from esearch.core.models.llm import load_llm

ML_MODELS = {}


def get_lifespan(
    app_settings: AppSettings,
) -> Callable[[FastAPI], _AsyncGeneratorContextManager]:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator:  # noqa: ARG001
        # Load the ML model
        ML_MODELS["embedder"] = load_embedder(app_settings.embedder_model_name)
        ML_MODELS["llm"] = load_llm(app_settings)
        yield
        # Clean up the ML models and release the resources
        ML_MODELS.clear()

    return lifespan
