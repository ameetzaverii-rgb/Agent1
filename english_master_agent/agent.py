#!/usr/bin/env python3
"""CLI chat loop for Professor Lex, the master English-teaching agent.

Usage:
    export ANTHROPIC_API_KEY=sk-...
    python agent.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from anthropic import Anthropic

MODEL = os.environ.get("ENGLISH_AGENT_MODEL", "claude-sonnet-4-5")
SYSTEM_PROMPT_PATH = Path(__file__).parent / "system_prompt.md"
MAX_TOKENS = 2048


def load_system_prompt() -> str:
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def main() -> None:
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Error: set the ANTHROPIC_API_KEY environment variable first.", file=sys.stderr)
        sys.exit(1)

    client = Anthropic()
    system_prompt = load_system_prompt()
    history: list[dict] = []

    print("Professor Lex is ready. Type in English (or your own language) to begin.")
    print("Type 'exit' or 'quit' to end the session.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        history.append({"role": "user", "content": user_input})

        print("Professor Lex: ", end="", flush=True)
        reply_parts: list[str] = []
        with client.messages.stream(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=history,
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                reply_parts.append(text)
        print("\n")

        history.append({"role": "assistant", "content": "".join(reply_parts)})


if __name__ == "__main__":
    main()
