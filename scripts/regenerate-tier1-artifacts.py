"""Regenerate all Tier 1a committed artifacts from canonical plugins/.

Run as: python scripts/regenerate-tier1-artifacts.py [--check]
"""

import argparse
import json
from pathlib import Path

from agent_forge.canonical import discover_plugins
from agent_forge.translators.copilot_cli import (
    build_copilot_marketplace_json,
    build_copilot_plugin_json,
)
from agent_forge.translators.codex_cli import (
    build_codex_marketplace_json,
    build_codex_plugin_json,
    md_agent_to_toml,
)
from agent_forge.translators.cursor import (
    build_cursor_marketplace_json,
    build_cursor_plugin_json,
)
from agent_forge.translators.factory_droid import (
    build_droid_marketplace_json,
    build_droid_plugin_json,
)

REPO = Path(__file__).resolve().parent.parent


def regenerate_copilot(check: bool) -> bool:
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = discover_plugins(REPO / "plugins")
    out_marketplace = REPO / ".github/plugin/marketplace.json"
    out_marketplace.parent.mkdir(parents=True, exist_ok=True)
    new_content = json.dumps(
        build_copilot_marketplace_json(canonical, plugins),
        indent=2,
    ) + "\n"
    drifted = False
    if check and out_marketplace.exists():
        if out_marketplace.read_text() != new_content:
            print(f"DRIFT: {out_marketplace}")
            drifted = True
    else:
        out_marketplace.write_text(new_content)
    for plugin in plugins:
        plugin_json = plugin.plugin_dir / "plugin.json"
        new_pj = json.dumps(build_copilot_plugin_json(plugin), indent=2) + "\n"
        if check and plugin_json.exists():
            if plugin_json.read_text() != new_pj:
                print(f"DRIFT: {plugin_json}")
                drifted = True
        else:
            plugin_json.write_text(new_pj)
        agents_dir = plugin.plugin_dir / "agents"
        if agents_dir.exists():
            for src in agents_dir.glob("*.md"):
                if src.stem.endswith(".agent"):
                    continue
                dst = agents_dir / f"{src.stem}.agent.md"
                if check and dst.exists():
                    if dst.read_bytes() != src.read_bytes():
                        print(f"DRIFT: {dst}")
                        drifted = True
                else:
                    dst.write_bytes(src.read_bytes())
    return drifted


def regenerate_codex(check: bool) -> bool:
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = discover_plugins(REPO / "plugins")
    out_marketplace = REPO / ".codex-plugin/marketplace.json"
    out_marketplace.parent.mkdir(parents=True, exist_ok=True)
    new_content = json.dumps(build_codex_marketplace_json(canonical, plugins), indent=2) + "\n"
    drifted = False
    if check and out_marketplace.exists():
        if out_marketplace.read_text() != new_content:
            print(f"DRIFT: {out_marketplace}")
            drifted = True
    else:
        out_marketplace.write_text(new_content)
    for plugin in plugins:
        plugin_json = plugin.plugin_dir / ".codex-plugin/plugin.json"
        plugin_json.parent.mkdir(parents=True, exist_ok=True)
        new_pj = json.dumps(build_codex_plugin_json(plugin), indent=2) + "\n"
        if check and plugin_json.exists():
            if plugin_json.read_text() != new_pj:
                print(f"DRIFT: {plugin_json}")
                drifted = True
        else:
            plugin_json.write_text(new_pj)
        agents_dir = plugin.plugin_dir / "agents"
        if agents_dir.exists():
            for src in agents_dir.glob("*.md"):
                if src.stem.endswith(".agent"):
                    continue
                dst = agents_dir / f"{src.stem}.toml"
                new_toml = md_agent_to_toml(src)
                if check and dst.exists():
                    if dst.read_text() != new_toml:
                        print(f"DRIFT: {dst}")
                        drifted = True
                else:
                    dst.write_text(new_toml)
    return drifted


def regenerate_cursor(check: bool) -> bool:
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = discover_plugins(REPO / "plugins")
    out_marketplace = REPO / ".cursor-plugin/marketplace.json"
    out_marketplace.parent.mkdir(parents=True, exist_ok=True)
    new_content = json.dumps(build_cursor_marketplace_json(canonical, plugins), indent=2) + "\n"
    drifted = False
    if check and out_marketplace.exists():
        if out_marketplace.read_text() != new_content:
            print(f"DRIFT: {out_marketplace}")
            drifted = True
    else:
        out_marketplace.write_text(new_content)
    for plugin in plugins:
        plugin_json = plugin.plugin_dir / ".cursor-plugin/plugin.json"
        plugin_json.parent.mkdir(parents=True, exist_ok=True)
        new_pj = json.dumps(build_cursor_plugin_json(plugin), indent=2) + "\n"
        if check and plugin_json.exists():
            if plugin_json.read_text() != new_pj:
                print(f"DRIFT: {plugin_json}")
                drifted = True
        else:
            plugin_json.write_text(new_pj)
    return drifted


def regenerate_droid(check: bool) -> bool:
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = discover_plugins(REPO / "plugins")
    out_marketplace = REPO / ".factory-plugin/marketplace.json"
    out_marketplace.parent.mkdir(parents=True, exist_ok=True)
    new_content = json.dumps(build_droid_marketplace_json(canonical, plugins), indent=2) + "\n"
    drifted = False
    if check and out_marketplace.exists():
        if out_marketplace.read_text() != new_content:
            print(f"DRIFT: {out_marketplace}")
            drifted = True
    else:
        out_marketplace.write_text(new_content)
    for plugin in plugins:
        plugin_json = plugin.plugin_dir / ".factory-plugin/plugin.json"
        plugin_json.parent.mkdir(parents=True, exist_ok=True)
        new_pj = json.dumps(build_droid_plugin_json(plugin), indent=2) + "\n"
        if check and plugin_json.exists():
            if plugin_json.read_text() != new_pj:
                print(f"DRIFT: {plugin_json}")
                drifted = True
        else:
            plugin_json.write_text(new_pj)
    return drifted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="Exit non-zero if any committed artifact would change.")
    args = parser.parse_args()
    drifted = False
    drifted = regenerate_copilot(args.check) or drifted
    drifted = regenerate_codex(args.check) or drifted
    drifted = regenerate_cursor(args.check) or drifted
    drifted = regenerate_droid(args.check) or drifted
    if args.check and drifted:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
