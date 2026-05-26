"""tests/unit/translators/test_prompt_loader.py"""

from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.prompt_loader import build_loader_md

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_prompt_loader_registered() -> None:
    t = get_translator("prompt-loader")
    assert t.tier == "3"


def test_loader_includes_frontmatter_for_routing() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="tqnonline/agent-forge", branch="main")
    assert loader.startswith("---\n")
    assert "name: humanize" in loader
    assert "description:" in loader


def test_loader_links_to_raw_skill_md() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="tqnonline/agent-forge", branch="main")
    expected = "https://raw.githubusercontent.com/tqnonline/agent-forge/main/plugins/writing/skills/humanize/SKILL.md"
    assert expected in loader


def test_loader_links_each_reference() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="tqnonline/agent-forge", branch="main")
    for ref in skill.references():
        rel = ref.relative_to(REPO).as_posix()
        assert f"https://raw.githubusercontent.com/tqnonline/agent-forge/main/{rel}" in loader


def test_loader_instructs_lazy_reference_loading() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    skill = next(s for s in plugins["writing"].skills() if s.name == "humanize")
    loader = build_loader_md(skill, repo="tqnonline/agent-forge", branch="main")
    assert "Do NOT eagerly fetch references" in loader
