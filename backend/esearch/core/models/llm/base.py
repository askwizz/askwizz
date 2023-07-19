from typing import Any, Callable, Coroutine


class LLMModel:
    async def answer_prompt(
        self: "LLMModel",
        prompt: str,
        callback: Callable[[str], Coroutine[Any, Any, None]] | None = None,
    ) -> str:
        raise NotImplementedError()
