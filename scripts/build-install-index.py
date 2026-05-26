"""Generate docs/install/_index.md — catalog of all plugins × all install targets.

Usage:
  python scripts/build-install-index.py [--check]
"""

import argparse
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
INDEX = REPO / "docs/install/_index.md"

INSTALL_TARGETS = [
    ("Claude Code", "claude-code", "1a"),
    ("GitHub Copilot CLI", "github-copilot-cli", "1a"),
    ("Codex CLI", "codex-cli", "1a"),
    ("Cursor", "cursor", "1a"),
    ("Factory.ai Droid", "factory-droid", "1a"),
    ("Amp", "amp", "1b"),
    ("Gemini CLI", "gemini-cli", "1b"),
    ("Kilo Code", "kilocode", "2"),
    ("OpenCode", "opencode", "2"),
    ("Crush", "crush", "2"),
    ("Perplexity Spaces", "perplexity", "3"),
    ("ChatGPT custom GPTs", "chatgpt-gpts", "3"),
    ("Claude.ai Projects", "claude-projects", "3"),
]


def build() -> str:
    canonical = json.loads((REPO / ".claude-plugin/marketplace.json").read_text())
    plugins = canonical["plugins"]
    out = ["# agent-forge install catalog\n\n"]
    out.append("> Paste this URL into any LLM agent to install:\n")
    out.append("> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/<tool>.md`\n\n")
    out.append(f"## Install targets ({len(INSTALL_TARGETS)})\n\n")
    out.append("| Tool | Tier | Install guide |\n")
    out.append("|---|---|---|\n")
    for name, slug, tier in INSTALL_TARGETS:
        out.append(f"| {name} | {tier} | [{slug}.md](./{slug}.md) |\n")
    out.append("\n## Plugins (4 at v1.0)\n\n")
    for p in plugins:
        out.append(f"### {p['name']}\n\n{p['description']}\n\n")
        out.append("Install for Claude Code:\n```bash\nclaude plugin install " + p['name'] + "\n```\n\n")
        out.append(f"Install for any other tool — see the [per-tool guide](claude-code.md).\n\n")
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        actual = INDEX.read_text() if INDEX.exists() else ""
        if actual != expected:
            print("docs/install/_index.md drifted from canonical sources")
            raise SystemExit(1)
    else:
        INDEX.parent.mkdir(parents=True, exist_ok=True)
        INDEX.write_text(expected)


if __name__ == "__main__":
    main()
