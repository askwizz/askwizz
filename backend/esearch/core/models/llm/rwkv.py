import asyncio
import os
from typing import Any, Callable, Coroutine, Type

from rwkv.model import RWKV
from rwkv.utils import PIPELINE, PIPELINE_ARGS

from esearch.core.models.llm.base import LLMModel


class CustomPipeline(PIPELINE):
    async def generate(  # noqa: PLR0913
        self: "CustomPipeline",
        ctx: str,
        token_count: int = 100,
        args: PIPELINE_ARGS = PIPELINE_ARGS(),  # noqa: B008
        callback: Callable[[str], Coroutine[Any, Any, None]] | None = None,
        state: Any = None,  # noqa: ANN401
    ) -> str:
        all_tokens = []
        out_last = 0
        out_str = ""
        occurrence = {}
        token = ""
        out = {}
        for i in range(token_count):
            # forward & adjust prob.
            tokens = self.encode(ctx) if i == 0 else [token]
            while len(tokens) > 0:
                out, state = self.model.forward(tokens[: args.chunk_len], state)
                tokens = tokens[args.chunk_len :]

            for n in args.token_ban:
                out[n] = -float("inf")
            for n in occurrence:
                out[n] -= args.alpha_presence + occurrence[n] * args.alpha_frequency

            # sampler
            token = self.sample_logits(
                out, temperature=args.temperature, top_p=args.top_p, top_k=args.top_k
            )
            if token in args.token_stop:
                break
            all_tokens += [token]
            if token not in occurrence:
                occurrence[token] = 1
            else:
                occurrence[token] += 1

            # output
            tmp: str = self.decode(all_tokens[out_last:])
            if "\ufffd" not in tmp:  # is valid utf-8 string?
                if callback:
                    await callback(tmp)  # type: ignore
                    await asyncio.sleep(0)
                out_str += tmp
                out_last = i + 1
        return out_str


class RWKVLLMModel(LLMModel):
    def __init__(self: "RWKVLLMModel", path: str) -> None:
        model = RWKV(
            model=path,
            strategy="cpu fp32",
        )
        token_config_path = os.path.join(
            os.path.dirname(__file__), "20B_tokenizer.json"
        )
        pipeline = CustomPipeline(model, token_config_path)
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
    def from_path(cls: Type["RWKVLLMModel"], path: str) -> "RWKVLLMModel":
        return cls(path=path)

    async def answer_prompt(
        self: "RWKVLLMModel",
        prompt: str,
        callback: Callable[[str], Coroutine[Any, Any, None]] | None = None,
    ) -> str:
        return await self.pipeline.generate(
            prompt,
            args=self.args,
            callback=callback,
            token_count=50,
        )
