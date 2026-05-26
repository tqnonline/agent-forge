# Installing agent-forge plugins for Claude Code

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/claude-code.md`

## Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- Optional: `agent-forge` Python CLI (`pipx install agent-forge`) for unified update tracking

## Quick install

### Option A: Native install command (recommended)

```bash
# Register the agent-forge marketplace
claude plugin marketplace add github:tqnonline/agent-forge

# Install individual plugins
claude plugin install writing
claude plugin install prompts
claude plugin install msft-arch
claude plugin install pm
```

### Option B: Via the agent-forge CLI

```bash
pipx install agent-forge
agent-forge install writing --tier claude-code
```

## Verify

```bash
claude plugin list
```
Expected: agent-forge plugins (writing, prompts, msft-arch, pm) listed with version and status.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `~/.claude/skills/` | Loaded on demand via frontmatter routing |
| Agents | `.claude/agents/*.md` | Exposed as sub-agents in Claude Code |
| Commands | `.claude/commands/*.md` | Exposed as slash commands in Claude Code |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

Native alternative:
```bash
claude plugin update writing
claude plugin update --all
```

## Removing

```bash
agent-forge remove writing@claude-code
# or native:
claude plugin remove writing
```

## Troubleshooting

**Plugin not appearing after install:**
1. Run `claude plugin list` — if not listed, re-run `claude plugin marketplace add github:tqnonline/agent-forge`
2. Restart Claude Code; skills load at session start from `~/.claude/skills/`

**Skill not triggering:**
1. Check the SKILL.md frontmatter description — it controls when Claude routes to the skill
2. Try invoking explicitly: `use the humanize skill to rewrite this`

**See also:** [Contributing](../contributing/adding-a-plugin.md)
