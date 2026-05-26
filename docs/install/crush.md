# Installing agent-forge plugins for Crush

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/crush.md`

## Prerequisites

- Crush installed (`brew install charmbracelet/tap/crush` or from `charm.sh/crush`)
- Python 3.9+ and `pipx` (`pip install pipx`)
- Anthropic API key or compatible model provider configured

## Quick install

### Via the agent-forge CLI (only method for Crush)

```bash
pipx install tqn-agent-forge

# Install individual plugins
agent-forge install writing --tier crush
agent-forge install prompts --tier crush
agent-forge install msft-arch --tier crush
agent-forge install pm --tier crush
```

Skills are copied to `~/.claude/skills/<plugin>/` — Crush reads from the same
directory as Claude Code.

## Verify

Open Crush and run:

```bash
/skills
```

Expected: agent-forge skills listed (humanize, prompt-forge, and others).

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `~/.claude/skills/writing/` | Crush reads Claude's skill directory |
| Skills | `~/.claude/skills/prompts/` | One directory per plugin |
| Skills | `~/.claude/skills/msft-arch/` | All SKILL.md files present |
| Skills | `~/.claude/skills/pm/` | Frontmatter routing preserved |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

## Removing

```bash
agent-forge remove writing@crush
```

## Troubleshooting

**Skills not appearing after install:**
1. Restart Crush — skills are loaded at session start
2. Confirm `~/.claude/skills/writing/` exists: `ls ~/.claude/skills/`

**`agent-forge` command not found:**
1. Check pipx installed correctly: `pipx list`
2. Ensure `~/.local/bin` is on your `$PATH`: `export PATH="$HOME/.local/bin:$PATH"`

**See also:** [Contributing](../contributing/adding-a-plugin.md)
