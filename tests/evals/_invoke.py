"""Invoke a skill against Claude Haiku 4.5 and return its output."""

import os

import anthropic

INVOKE_MODEL = os.environ.get("EVAL_INVOKE_MODEL", "claude-haiku-4-5-20251001")


def invoke_skill(skill_body: str, user_input: str, context: str | None = None) -> str:
    client = anthropic.Anthropic(max_retries=5)
    user_message = user_input
    if context:
        user_message = f"Context: {context}\n\nInput:\n{user_input}"
    message = client.messages.create(
        model=INVOKE_MODEL,
        max_tokens=2000,
        system=skill_body,
        messages=[{"role": "user", "content": user_message}],
    )
    return message.content[0].text
