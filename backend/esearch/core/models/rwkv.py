import os
from typing import Callable, Type

from rwkv.model import RWKV
from rwkv.utils import PIPELINE, PIPELINE_ARGS


# todo - see if langchain already provides abtractions
class LLMModel:
    def __init__(self: "LLMModel", path: str) -> None:
        model = RWKV(
            model=path,
            strategy="cpu fp32",
        )
        token_config_path = os.path.join(
            os.path.dirname(__file__), "20B_tokenizer.json"
        )
        pipeline = PIPELINE(model, token_config_path)
        args = PIPELINE_ARGS(
            temperature=0.2,
            top_p=0.7,
            top_k=100,  # top_k = 0 then ignore
            alpha_frequency=0.25,
            alpha_presence=0.25,
            token_ban=[],  # ban the generation of some tokens
            token_stop=[0],  # stop generation whenever you see any token here
            chunk_len=256,
        )

        self.model_path = path
        self.pipeline = pipeline
        self.args = args

    @classmethod
    def from_path(cls: Type["LLMModel"], path: str) -> "LLMModel":
        return cls(path=path)

    def answer_prompt(
        self: "LLMModel", prompt: str, callback: Callable[[str], None]
    ) -> str:
        return self.pipeline.generate(
            prompt, args=self.args, callback=callback, token_count=50
        )
