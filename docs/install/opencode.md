# Installing agent-forge plugins for OpenCode

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/opencode.md`

## Prerequisites

- OpenCode installed (`npm install -g opencode-ai` or from `opencode.ai`)
- Python 3.9+ and `pipx` (`pip install pipx`)
- API key configured for your preferred model provider

## Quick install

### Via the agent-forge CLI (only method for OpenCode)

```bash
pipx install tqn-agent-forge   # or: uv tool install tqn-agent-forge

# Install individual plugins
agent-forge install writing --tier opencode
agent-forge install prompts --tier opencode
agent-forge install msft-arch --tier opencode
agent-forge install pm --tier opencode
```

Skills are copied to `~/.claude/skills/<plugin>/` — OpenCode reads from the same
location as Claude Code.

## Verify

```bash
opencode
# Once in the REPL:
/skills list
```

Expected: agent-forge skills (humanize, prompt-forge, and others) listed.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `~/.claude/skills/writing/` | OpenCode reads Claude's skill directory |
| Skills | `~/.claude/skills/prompts/` | One directory per plugin |
| Skills | `~/.claude/skills/msft-arch/` | Includes all SKILL.md files |
| Skills | `~/.claude/skills/pm/` | Frontmatter routing active |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

## Removing

```bash
agent-forge remove writing@opencode
```

## Troubleshooting

**Skills not showing in `/skills list`:**
1. Exit and restart OpenCode — skills are indexed at startup
2. Check `~/.claude/skills/writing/` exists and is non-empty

**Skill invocation fails:**
1. Verify your model API key is valid (`opencode --check-auth`)
2. Try invoking the skill explicitly: `use the humanize skill`

**See also:** [Contributing](../contributing/adding-a-plugin.md)
