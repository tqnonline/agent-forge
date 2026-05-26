# Installing agent-forge plugins for Factory.ai Droid

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/factory-droid.md`

Covers both the **droid CLI** and the **Factory desktop app** — they share
`~/.factory/` configuration and consume the same plugin layout.

## Prerequisites

- Droid CLI installed (https://factory.ai/product/cli) — or the Factory
  desktop app (https://factory.ai/news/factory-desktop)
- Optional: `agent-forge` Python CLI (`pipx install tqn-agent-forge`) for
  unified update tracking across CLIs

## Quick install

### Option A: Native install command (recommended)

```bash
# Register the agent-forge marketplace
droid plugin marketplace add https://github.com/tqnonline/agent-forge

# Install individual plugins (marketplace name is `agent-forge`)
droid plugin install writing@agent-forge
droid plugin install prompts@agent-forge
droid plugin install msft-arch@agent-forge
droid plugin install pm@agent-forge
```

### Option B: Via the agent-forge CLI

```bash
pipx install tqn-agent-forge   # or: uv tool install tqn-agent-forge
agent-forge install writing --tier factory-droid
```

## Desktop app

The Factory desktop app reads the same `~/.factory/` directory the CLI writes
to. After running the droid CLI commands above, restart the desktop app and the
plugins appear automatically. No separate install path.

## Verify

```bash
droid plugin list
```
Expected: agent-forge plugins (writing, prompts, msft-arch, pm) listed.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `~/.factory/skills/` or per-project `.factory/skills/` | Invoked on demand by SKILL.md frontmatter |
| Custom droids | `~/.factory/droids/*.md` | Subagent definitions |
| Commands | Plugin's `commands/*.md` | Slash commands |
| MCP servers | Plugin's `mcp.json` | Auto-registered |

Droid is documented as "compatible with plugins built for Claude Code," so the
same canonical plugin layout works without conversion.

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

Native alternative:
```bash
droid plugin update writing
droid plugin marketplace update agent-forge
```

## Removing

```bash
agent-forge remove writing@factory-droid
# or native:
droid plugin uninstall writing
```

## Troubleshooting

**Plugin not appearing after install:**
1. Run `droid plugin list` — if not listed, re-add the marketplace:
   `droid plugin marketplace add https://github.com/tqnonline/agent-forge`
2. Restart droid CLI or the Factory desktop app

**"Custom droids disabled":**
Enable via `/settings → Experimental → Custom Droids` in droid, or set
`"enableCustomDroids": true` in `~/.factory/settings.json`.

**Skill not triggering:**
1. Check the SKILL.md frontmatter `description` — it controls when droid routes
   to the skill
2. Try invoking explicitly: `use the humanize skill to rewrite this`

**See also:** [Contributing](../contributing/adding-a-plugin.md)
