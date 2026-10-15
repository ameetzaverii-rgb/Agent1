"""
Base class for all specialist agents.
Each agent is an async function that calls Claude and returns structured JSON.
"""

import json
import anthropic
from typing import Any, Dict

CLIENT = anthropic.Anthropic()
MODEL = "claude-opus-4-8"


async def run_agent(
    agent_name: str,
    system_prompt: str,
    user_prompt: str,
    use_thinking: bool = False,
    thinking_budget: int = 8000,
    max_tokens: int = 8000,
) -> Dict[str, Any]:
    """
    Core call wrapper. Returns parsed JSON dict from the agent's response.
    Falls back to {"raw": text} if JSON parsing fails.
    """
    kwargs: Dict[str, Any] = {
        "model": MODEL,
        "max_tokens": max_tokens,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
    }
    if use_thinking:
        kwargs["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget}

    response = CLIENT.messages.create(**kwargs)
    text = next((b.text for b in response.content if b.type == "text"), "")
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text, "agent": agent_name}
