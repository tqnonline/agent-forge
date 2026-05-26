# Installing agent-forge plugins for Kilo Code

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/kilocode.md`

## Prerequisites

- Kilo Code VS Code extension installed (search "Kilo Code" in VS Code Marketplace)
- Python 3.9+ and `pipx` (`pip install pipx`)
- Optional: API key for your preferred model provider

## Quick install

### Via the agent-forge CLI (only method for Kilo Code)

```bash
pipx install tqn-agent-forge

# Install individual plugins
agent-forge install writing --tier kilocode
agent-forge install prompts --tier kilocode
agent-forge install msft-arch --tier kilocode
agent-forge install pm --tier kilocode
```

Kilo Code reads skills from Claude Code's skill directory, so this command copies
the canonical SKILL.md files into `~/.claude/skills/<plugin>/`.

## Verify

Open VS Code with Kilo Code extension → Skills panel. The installed plugins should appear
in the skill list. Alternatively:

```bash
ls ~/.claude/skills/
```

Expected: `writing/`, `prompts/`, `msft-arch/`, `pm/` directories present.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `~/.claude/skills/writing/` | Kilo Code reads Claude's skill directory |
| Skills | `~/.claude/skills/prompts/` | One directory per plugin |
| Skills | `~/.claude/skills/msft-arch/` | All SKILL.md files copied |
| Skills | `~/.claude/skills/pm/` | Frontmatter routing preserved |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply (re-copies from latest SHA)
```

## Removing

```bash
agent-forge remove writing@kilocode
# Removes ~/.claude/skills/writing/ if not used by other tools
```

## Troubleshooting

**Skills not appearing in Kilo Code Skills panel:**
1. Restart VS Code after install — Kilo Code reloads skills on startup
2. Confirm `~/.claude/skills/writing/` exists and contains `humanize/SKILL.md`

**install command not found:**
1. Run `pipx install tqn-agent-forge` and verify `~/.local/bin` is on your PATH
2. Try `python -m agent_forge install writing --tier kilocode`

**See also:** [Contributing](../contributing/adding-a-plugin.md)
