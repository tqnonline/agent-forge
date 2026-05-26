"""Translator registry — every CLI's translator registers itself here."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent_forge.translators._base import Translator

_REGISTRY: dict[str, "Translator"] = {}


def register(translator: "Translator") -> "Translator":
    _REGISTRY[translator.name] = translator
    return translator


def get_translator(name: str) -> "Translator":
    if name not in _REGISTRY:
        raise KeyError(f"unknown CLI: {name}; available: {sorted(_REGISTRY)}")
    return _REGISTRY[name]


def registered_translators() -> list[str]:
    return sorted(_REGISTRY)


# Lazy import to populate registry — must come after _REGISTRY is defined
from agent_forge.translators import (  # noqa: E402,F401
    claude_code,
    copilot_cli,
    codex_cli,
    cursor,
    factory_droid,
    amp,
    gemini_cli,
    kilocode,
    opencode,
    crush,
    prompt_loader,
)
