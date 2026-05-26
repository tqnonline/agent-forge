"""Factory.ai droid translator (Tier 1a — registry-style native marketplace).

Covers the droid CLI and Factory desktop app (both share ~/.factory/ config
and consume the same plugin layout). Droid is documented as "compatible with
plugins built for Claude Code," so this translator is a thin metadata wrapper
around the canonical Claude format.

Marketplace registry:  .factory-plugin/marketplace.json
Per-plugin manifest:   plugins/<name>/.factory-plugin/plugin.json
Install commands:
    droid plugin marketplace add https://github.com/<owner>/<repo>
    droid plugin install <plugin>@<marketplace-name>
"""

import shutil
from pathlib import Path

from agent_forge.canonical import CanonicalPlugin
from agent_forge.translators import register


_DEFAULT_CATEGORY = "productivity"
_CATEGORY_OVERRIDES: dict[str, str] = {
    # plugin name -> droid marketplace category
    "writing": "productivity",
    "prompts": "productivity",
    "msft-arch": "engineering",
    "pm": "productivity",
}


def _category_for(name: str) -> str:
    return _CATEGORY_OVERRIDES.get(name, _DEFAULT_CATEGORY)


def build_droid_marketplace_json(canonical: dict, plugins: list[CanonicalPlugin]) -> dict:
    """Top-level .factory-plugin/marketplace.json — droid plugin marketplace add."""
    return {
        "name": canonical["name"],
        "description": canonical["description"],
        "owner": canonical["owner"],
        "plugins": [
            {
                "name": p.name,
                "description": p.manifest.get("description", ""),
                "source": f"./plugins/{p.name}",
                "category": _category_for(p.name),
            }
            for p in plugins
        ],
    }


def build_droid_plugin_json(plugin: CanonicalPlugin) -> dict:
    """Per-plugin .factory-plugin/plugin.json."""
    pj: dict = {
        "name": plugin.name,
        "description": plugin.manifest.get("description", ""),
        "version": plugin.manifest.get("version", "1.0.0"),
    }
    if author := plugin.manifest.get("author"):
        pj["author"] = author
    return pj


class FactoryDroidTranslator:
    name = "factory-droid"
    tier = "1a"

    def detect(self) -> bool:
        if shutil.which("droid"):
            return True
        # Factory desktop app stores config under ~/.factory regardless of CLI install
        return Path.home().joinpath(".factory").exists()

    def install_command(self, repo: str, marketplace_name: str | None = None) -> str:
        """Human-readable install snippet, used in install docs."""
        mp = marketplace_name or repo.split("/")[-1]
        return (
            f"droid plugin marketplace add https://github.com/{repo}\n"
            f"droid plugin install <plugin>@{mp}"
        )

    def target_paths(self, plugin_root: Path) -> dict[str, Path]:
        return {}

    def translate_skill(self, skill_dir: Path, dest: Path) -> None:
        pass

    def translate_agent(self, agent_md: Path, dest: Path) -> None:
        pass

    def translate_command(self, command_md: Path, dest: Path) -> None:
        pass

    def post_install_verify(self, plugin: str) -> bool:
        return True


register(FactoryDroidTranslator())
