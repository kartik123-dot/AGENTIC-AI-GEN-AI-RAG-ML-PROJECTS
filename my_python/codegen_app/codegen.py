"""Core logic: talk to the Anthropic API and post-process the output."""
import os
import re
from typing import Iterator

import anthropic
from dotenv import load_dotenv

from prompts import build_system_prompt

load_dotenv()


def get_client(api_key: str | None = None) -> anthropic.Anthropic:
    key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("No API key found. Enter it in the sidebar or set ANTHROPIC_API_KEY in .env")
    return anthropic.Anthropic(api_key=key)


def stream_code(client: anthropic.Anthropic, user_request: str, params: dict,
                history: list[dict] | None = None) -> Iterator[str]:
    """Yield text chunks as the model generates them."""
    messages = (history or []) + [{"role": "user", "content": user_request}]
    with client.messages.stream(
        model=params["model"],
        max_tokens=params["max_tokens"],
        temperature=params["temperature"],
        system=build_system_prompt(params),
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def extract_code_blocks(text: str) -> list[tuple[str, str]]:
    """Return [(language, code), ...] from markdown fenced blocks."""
    return [(lang or "", code.strip()) for lang, code in
            re.findall(r"```(\w+)?\n(.*?)```", text, flags=re.DOTALL)]
