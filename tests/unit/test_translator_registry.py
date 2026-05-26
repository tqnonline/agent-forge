"""tests/unit/test_translator_registry.py"""

from agent_forge.translators import get_translator, registered_translators


def test_registry_lists_all_v1_targets() -> None:
    names = registered_translators()
    assert set(names) == {
        "claude-code", "copilot-cli", "codex-cli", "cursor", "factory-droid",  # Tier 1a
        "amp", "gemini-cli",                                                     # Tier 1b
        "kilocode", "opencode", "crush",                                         # Tier 2
        "prompt-loader",                                                         # Tier 3
    }


def test_get_translator_returns_instance() -> None:
    t = get_translator("claude-code")
    assert t.name == "claude-code"
    assert t.tier == "1a"


def test_get_translator_raises_on_unknown() -> None:
    import pytest
    with pytest.raises(KeyError, match="unknown CLI"):
        get_translator("nonexistent-cli")
