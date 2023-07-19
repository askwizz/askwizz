import asyncio
from typing import Any, Callable, Coroutine, Iterator

from llama_cpp import CompletionChunk, Llama

from esearch.core.models.llm.base import LLMModel


class LLama2LLM(LLMModel):
    def __init__(self: "LLama2LLM", path: str) -> None:
        self.llm = Llama(model_path=path, n_ctx=4096)

    async def answer_prompt(
        self: "LLama2LLM",
        prompt: str,
        callback: Callable[[str], Coroutine[Any, Any, None]] | None = None,
    ) -> str:
        generator: Iterator[CompletionChunk] = self.llm(
            prompt,
            temperature=0.7,
            max_tokens=256,
            stop=["\n\n\n\n\n", "?", "Expert answer 2"],
            stream=True,
        )  # type: ignore
        answer = ""
        for token_generated in generator:
            token_text = token_generated["choices"][0]["text"]
            if callback:
                await callback(token_text)
                await asyncio.sleep(0)
            answer += token_text
        return answer
