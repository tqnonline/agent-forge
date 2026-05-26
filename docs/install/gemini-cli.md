# Installing agent-forge plugins for Gemini CLI

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/gemini-cli.md`

## Prerequisites

- Gemini CLI installed (`npm install -g @google/gemini-cli`)
- Google account authenticated (`gemini auth login`)
- Optional: `agent-forge` Python CLI (`pipx install tqn-agent-forge`) for unified update tracking

## Quick install

### Option A: Native git URL install (recommended)

```bash
# Install the full agent-forge marketplace via git URL
gemini skills install github:tqnonline/agent-forge

# Or install a specific plugin
gemini skills install github:tqnonline/agent-forge#plugins/writing
```

### Option B: Via the agent-forge CLI

```bash
pipx install tqn-agent-forge
agent-forge install writing --tier gemini-cli
```

## Verify

```bash
gemini skills list
```
Expected: agent-forge skills listed with source URL and current SHA.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `~/.gemini/skills/` | Cloned from git URL; loaded at session start |
| Agents | `~/.gemini/agents/` | Available as Gemini agent configurations |
| Commands | Invoked as `gemini run <skill-name>` | All installed skills accessible by name |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

Native alternative:
```bash
gemini skills update github:tqnonline/agent-forge
```

## Removing

```bash
agent-forge remove writing@gemini-cli
# or native:
gemini skills remove agent-forge
```

## Troubleshooting

**Skills not listed after install:**
1. Run `gemini auth status` — expired auth blocks the git clone
2. Check `~/.gemini/skills/` for the cloned directory

**Version mismatch:**
1. Run `gemini --version` — skills require Gemini CLI 1.0+
2. Update with `npm install -g @google/gemini-cli@latest`

**See also:** [Contributing](../contributing/adding-a-plugin.md)
