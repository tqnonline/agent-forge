"""tests/unit/translators/test_amp.py"""

from pathlib import Path

from agent_forge.translators import get_translator


def test_amp_translator_registered() -> None:
    t = get_translator("amp")
    assert t.tier == "1b"


def test_amp_install_command_string() -> None:
    t = get_translator("amp")
    cmd = t.install_command("tqnonline/agent-forge")
    assert cmd.startswith("amp skill add")
    assert "tqnonline/agent-forge" in cmd


def test_amp_translate_skill_is_noop(tmp_path: Path) -> None:
    t = get_translator("amp")
    t.translate_skill(tmp_path / "src", tmp_path / "dst")
    assert not (tmp_path / "dst").exists()
