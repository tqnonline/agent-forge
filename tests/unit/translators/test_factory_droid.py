"""tests/unit/translators/test_factory_droid.py"""

import json
from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators import get_translator
from agent_forge.translators.factory_droid import (
    build_droid_marketplace_json,
    build_droid_plugin_json,
)

REPO = Path(__file__).resolve().parent.parent.parent.parent


def test_factory_droid_translator_registered() -> None:
    t = get_translator("factory-droid")
    assert t.tier == "1a"


def test_factory_droid_install_command() -> None:
    t = get_translator("factory-droid")
    cmd = t.install_command("tqnonline/agent-forge")
    assert "droid plugin marketplace add" in cmd
    assert "tqnonline/agent-forge" in cmd
    assert "agent-forge" in cmd  # marketplace name defaults to repo name


def test_droid_marketplace_json_shape() -> None:
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    out = build_droid_marketplace_json(canonical, plugins)
    assert out["name"] == canonical["name"]
    assert "owner" in out
    assert "plugins" in out
    for p in out["plugins"]:
        assert {"name", "description", "source", "category"} <= set(p)
        assert p["source"].startswith("./plugins/")


def test_droid_plugin_json_minimal() -> None:
    plugins = {p.name: p for p in discover_plugins(REPO / "plugins")}
    pj = build_droid_plugin_json(plugins["writing"])
    assert pj["name"] == "writing"
    assert "description" in pj
    assert "version" in pj


def test_droid_marketplace_matches_committed() -> None:
    """Committed .factory-plugin/marketplace.json must equal a fresh regeneration."""
    plugins = discover_plugins(REPO / "plugins")
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    expected = build_droid_marketplace_json(canonical, plugins)
    actual = json.loads((REPO / ".factory-plugin/marketplace.json").read_text())
    assert actual == expected
