# Installing agent-forge plugins for Amp

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/amp.md`

## Prerequisites

- Amp installed (Sourcegraph Amp CLI — `npm install -g @sourcegraph/amp`)
- Optional: `agent-forge` Python CLI (`pipx install tqn-agent-forge`) for unified update tracking

## Quick install

### Option A: Native git URL install (recommended)

```bash
# Install the full agent-forge marketplace via git URL
amp skill add github:tqnonline/agent-forge

# Or install a specific plugin
amp skill add github:tqnonline/agent-forge#plugins/writing
```

### Option B: Via the agent-forge CLI

```bash
pipx install tqn-agent-forge   # or: uv tool install tqn-agent-forge
agent-forge install writing --tier amp
```

## Verify

```bash
amp skill list
```
Expected: agent-forge skills (humanize, prompt-forge, and others) listed with source URL and version SHA.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `~/.amp/skills/` | Cloned from git URL; loaded by skill name |
| Agents | `~/.amp/agents/` | Available as Amp agent modes |
| Commands | Available via Amp CLI | Invoked as `amp run <skill-name>` |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply (re-clones from latest SHA)
```

Native alternative:
```bash
amp skill update github:tqnonline/agent-forge
```

## Removing

```bash
agent-forge remove writing@amp
# or native:
amp skill remove agent-forge
```

## Troubleshooting

**Skill not found after install:**
1. Run `amp skill list` to confirm the git URL was cloned successfully
2. Check `~/.amp/skills/` — if the directory is missing, retry `amp skill add`

**Git clone fails:**
1. Confirm you have internet access and can reach `github.com`
2. If behind a proxy, set `HTTPS_PROXY` before running the install command

**See also:** [Contributing](../contributing/adding-a-plugin.md)
