"""Invoke a skill against Claude Haiku 4.5 and return its output.

`temperature=0` is set so the same (skill_body, user_input) pair produces the
same output across runs — required for the regression check downstream to
detect actual skill changes rather than sampling noise. Opus 4.x dropped the
`temperature` parameter, so we omit it when the invoke model name contains
"opus"; in that case, baseline runs are inherently non-deterministic and
should be regenerated whenever a regression is suspected.
"""

import os

import anthropic

INVOKE_MODEL = os.environ.get("EVAL_INVOKE_MODEL", "claude-haiku-4-5-20251001")


def invoke_skill(skill_body: str, user_input: str, context: str | None = None) -> str:
    client = anthropic.Anthropic(max_retries=5)
    user_message = user_input
    if context:
        user_message = f"Context: {context}\n\nInput:\n{user_input}"
    kwargs = {
        "model": INVOKE_MODEL,
        "max_tokens": 8000,
        "system": skill_body,
        "messages": [{"role": "user", "content": user_message}],
    }
    if "opus" not in INVOKE_MODEL.lower():
        kwargs["temperature"] = 0
    message = client.messages.create(**kwargs)
    return message.content[0].text
