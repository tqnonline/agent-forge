"""Invoke a skill, dispatching between two harnesses based on the skill path.

Two distinct skill shapes exist in this repo:

1. **Single-turn skills** — produce a self-contained text response in one pass.
   Examples: `writing/humanize` (rewrites a paragraph), `msft-arch/azure-architect`
   (single architecture recommendation). These score well on Haiku 4.5 at
   max_tokens=8000 with a plain single-turn call. Cheap.

2. **Multi-file / tool-use skills** — designed to call `Write`, `Read`,
   `AskUserQuestion`, etc. across multiple turns to produce a directory of
   artifacts. Examples: `msft-arch/spec` (writes spec/design/*.md), `pm/prd-draft`,
   `msft-arch/threat-model`. These get truncated under single-turn invocation
   because their real output sits inside Write tool calls. They need Sonnet 4.6
   (64K output ceiling) + a tool-stub agent loop.

`AGENT_LOOP_SKILLS` lists the skill paths that get the multi-turn Sonnet
treatment. The default set was chosen as "skills with avg <3.5 in the Haiku
single-turn baseline" — those that empirically benefit from the upgrade.
Override via `EVAL_AGENT_LOOP_SKILLS` env var (comma-separated paths) or
`EVAL_FORCE_ALL_AGENT_LOOP=1` to send everything through the agent loop.

Determinism: `temperature=0` on every call for non-Opus models. Opus 4.x
dropped the temperature parameter, so it's omitted when the model name contains
"opus".
"""

import json
import os

import anthropic

SINGLE_TURN_MODEL = os.environ.get("EVAL_INVOKE_MODEL", "claude-haiku-4-5-20251001")
AGENT_LOOP_MODEL = os.environ.get("EVAL_AGENT_LOOP_MODEL", "claude-sonnet-4-6")
SINGLE_TURN_MAX_TOKENS = int(os.environ.get("EVAL_MAX_TOKENS", "8000"))
AGENT_LOOP_MAX_TOKENS_PER_TURN = int(os.environ.get("EVAL_AGENT_LOOP_MAX_TOKENS", "16000"))
MAX_TURNS = int(os.environ.get("EVAL_MAX_TURNS", "8"))

# Skills that empirically benefit from the multi-turn Sonnet agent loop because
# their real output is multi-file tool calls. Add a skill path here when its
# baseline avg sits below ~3.5 and you've confirmed the agent loop lifts it.
_DEFAULT_AGENT_LOOP_SKILLS = frozenset({
    "msft-arch/defender-sentinel",
    "msft-arch/discover",
    "msft-arch/requirements",
    "msft-arch/security-architect",
    "msft-arch/spec",
    "msft-arch/sre-architect",
    "msft-arch/standards",
    "msft-arch/threat-model",
    "msft-arch/tom-architect",
    "msft-arch/validate",
    "pm/backlog-ado",
    "pm/backlog-decompose",
    "pm/backlog-github",
    "pm/backlog-linear",
    "pm/discover",
    "pm/epic-decompose",
    "pm/map",
    "pm/philosophy",
    "pm/prd-draft",
    "pm/prd-review",
    "pm/prd-validate",
    "pm/tom-architect",
    "prompts/prompt-forge",
})

_env_override = os.environ.get("EVAL_AGENT_LOOP_SKILLS")
if _env_override:
    AGENT_LOOP_SKILLS = frozenset(s.strip() for s in _env_override.split(",") if s.strip())
else:
    AGENT_LOOP_SKILLS = _DEFAULT_AGENT_LOOP_SKILLS

_FORCE_ALL = os.environ.get("EVAL_FORCE_ALL_AGENT_LOOP") == "1"

TOOLS = [
    {
        "name": "Write",
        "description": "Write content to a file at the given path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["file_path", "content"],
        },
    },
    {
        "name": "Read",
        "description": "Read the contents of a file at the given path.",
        "input_schema": {
            "type": "object",
            "properties": {"file_path": {"type": "string"}},
            "required": ["file_path"],
        },
    },
    {
        "name": "Edit",
        "description": "Edit a file by replacing old_string with new_string.",
        "input_schema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"},
                "old_string": {"type": "string"},
                "new_string": {"type": "string"},
            },
            "required": ["file_path", "old_string", "new_string"],
        },
    },
    {
        "name": "Bash",
        "description": "Execute a bash command and return its output.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
    {
        "name": "Grep",
        "description": "Search for a pattern in files.",
        "input_schema": {
            "type": "object",
            "properties": {"pattern": {"type": "string"}},
            "required": ["pattern"],
        },
    },
    {
        "name": "Glob",
        "description": "Find files matching a glob pattern.",
        "input_schema": {
            "type": "object",
            "properties": {"pattern": {"type": "string"}},
            "required": ["pattern"],
        },
    },
    {
        "name": "AskUserQuestion",
        "description": "Ask the user one or more clarifying questions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {"question": {"type": "string"}},
                        "required": ["question"],
                    },
                }
            },
            "required": ["questions"],
        },
    },
]


def _stub_tool_result(name: str, tool_input: dict) -> str:
    """Synthesize a plausible response so the skill can keep working."""
    if name == "Write":
        path = tool_input.get("file_path", "?")
        content_len = len(tool_input.get("content", ""))
        return f"Wrote {content_len} bytes to {path}."
    if name == "Read":
        path = tool_input.get("file_path", "?")
        return f"[eval stub] File at {path} is unavailable in eval mode. Proceed using the context already provided in the input."
    if name == "Edit":
        return f"Edited {tool_input.get('file_path', '?')}."
    if name == "Bash":
        cmd = tool_input.get("command", "")[:200]
        return f"[eval stub] Command not executed in eval mode: {cmd}"
    if name in {"Grep", "Glob"}:
        return f"[eval stub] No matches for pattern in eval mode. Proceed using only the input context."
    if name == "AskUserQuestion":
        return (
            "[eval stub] No interactive user available. All necessary context "
            "is in the input above. Use reasonable defaults and proceed with "
            "the work end-to-end. Do not ask further questions."
        )
    return f"[eval stub] Tool {name!r} not implemented; proceed without it."


def _single_turn(skill_body: str, user_message: str) -> str:
    client = anthropic.Anthropic(max_retries=5)
    kwargs = {
        "model": SINGLE_TURN_MODEL,
        "max_tokens": SINGLE_TURN_MAX_TOKENS,
        "system": skill_body,
        "messages": [{"role": "user", "content": user_message}],
    }
    if "opus" not in SINGLE_TURN_MODEL.lower():
        kwargs["temperature"] = 0
    message = client.messages.create(**kwargs)
    return message.content[0].text


def _agent_loop(skill_body: str, user_message: str) -> str:
    client = anthropic.Anthropic(max_retries=5)
    messages = [{"role": "user", "content": user_message}]
    text_chunks: list[str] = []
    tool_call_log: list[dict] = []

    for _ in range(MAX_TURNS):
        kwargs = {
            "model": AGENT_LOOP_MODEL,
            "max_tokens": AGENT_LOOP_MAX_TOKENS_PER_TURN,
            "system": skill_body,
            "tools": TOOLS,
            "messages": messages,
        }
        if "opus" not in AGENT_LOOP_MODEL.lower():
            kwargs["temperature"] = 0
        msg = client.messages.create(**kwargs)

        turn_tool_calls: list = []
        for block in msg.content:
            if block.type == "text":
                text_chunks.append(block.text)
            elif block.type == "tool_use":
                tool_call_log.append({"name": block.name, "input": block.input})
                turn_tool_calls.append(block)

        if msg.stop_reason != "tool_use":
            break

        messages.append({"role": "assistant", "content": msg.content})
        messages.append({
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": _stub_tool_result(call.name, call.input),
                }
                for call in turn_tool_calls
            ],
        })

    output_parts: list[str] = []
    if text_chunks:
        output_parts.append("\n\n".join(text_chunks))

    write_blocks: list[str] = []
    other_calls: list[dict] = []
    for call in tool_call_log:
        if call["name"] == "Write":
            path = call["input"].get("file_path", "(unknown path)")
            content = call["input"].get("content", "")
            write_blocks.append(f"=== File: {path} ===\n{content}")
        else:
            other_calls.append(call)
    if write_blocks:
        output_parts.append("\n\n".join(write_blocks))

    if other_calls:
        digest_lines = ["--- Other Tool Calls ---"]
        for call in other_calls:
            input_repr = json.dumps(call["input"], indent=2)
            if len(input_repr) > 500:
                input_repr = input_repr[:500] + "\n... [truncated]"
            digest_lines.append(f"\n{call['name']}: {input_repr}")
        output_parts.append("\n".join(digest_lines))

    return "\n\n".join(output_parts).strip()


def invoke_skill(
    skill_body: str,
    user_input: str,
    context: str | None = None,
    skill_path: str | None = None,
) -> str:
    user_message = user_input
    if context:
        user_message = f"Context: {context}\n\nInput:\n{user_input}"
    use_agent_loop = _FORCE_ALL or (skill_path is not None and skill_path in AGENT_LOOP_SKILLS)
    if use_agent_loop:
        return _agent_loop(skill_body, user_message)
    return _single_turn(skill_body, user_message)
