import logging
from typing import Literal

from esearch.api.settings import AppSettings
from esearch.core.models.llm.base import LLMModel
from esearch.core.models.llm.llama2 import LLama2LLM
from esearch.core.models.llm.rwkv import RWKVLLMModel

LLMName = Literal["rwkv", "llama-2-7b-8K", "llama-2-7b-2K"]


def load_llm(settings: AppSettings) -> LLMModel:
    logging.info(f"Loading llm {settings.llm_name}")
    match settings.llm_name:
        case "rwkv":
            return RWKVLLMModel.from_path(settings.llm_path)
        case "llama-2-7b-8K" | "llama-2-7b-2K":
            return LLama2LLM(settings.llm_path)
        case _:
            raise ValueError(f"Unknown model name: {settings.llm_name}")
