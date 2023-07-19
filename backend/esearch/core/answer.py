import logging
from typing import Any, Callable, Coroutine

from esearch.core.messages import QueryMessage
from esearch.core.models.llm.base import LLMModel

MAX_CONTEXT_SIZE = 2048


def get_context(query_message: QueryMessage) -> str:
    texts = []
    for i, text in enumerate(query_message.texts):
        texts.append(f"Part {i+1}: {text}")
    texts_shorter_than_max_length = []
    length = 0
    i = 0
    text = texts[0]
    while length - len(text) < MAX_CONTEXT_SIZE:
        texts_shorter_than_max_length.append(text)
        i += 1
        text = texts[i]
        length += len(text)
    return "\n".join(texts_shorter_than_max_length)


def generate_qa_prompt(question: str, context: str) -> str:
    return f"""Q & A
Given the following extracted parts of multiple documents and a question, create a final answer with references.
If you don't know the answer, just say that you don't know. Don't try to make up an answer.

DOCUMENTS:
{context}

QUESTION:
{question}
Detailed expert answer:
"""  # noqa: E501


async def provide_answers(
    llm: LLMModel,
    message: QueryMessage,
    callback: Callable[[str], Coroutine[Any, Any, None]],
) -> str:
    prompt = generate_qa_prompt(message.query, get_context(message))
    logging.info(f"Generating llm answer to prompt: {prompt}")
    return await llm.answer_prompt(prompt, callback)
