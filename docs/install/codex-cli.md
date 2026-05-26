# Installing agent-forge plugins for Codex CLI

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/codex-cli.md`

## Prerequisites

- Codex CLI installed (`npm install -g @openai/codex`)
- OpenAI API key set (`export OPENAI_API_KEY=sk-...`)
- Optional: `agent-forge` Python CLI (`pipx install tqn-agent-forge`) for unified update tracking

## Quick install

### Option A: Native install command (recommended)

```bash
# Register the agent-forge plugin marketplace
codex plugin marketplace add tqnonline/agent-forge

# Install individual plugins
codex plugin install writing
codex plugin install prompts
codex plugin install msft-arch
codex plugin install pm
```

### Option B: Via the agent-forge CLI

```bash
pipx install tqn-agent-forge   # or: uv tool install tqn-agent-forge
agent-forge install writing --tier codex-cli
```

## Verify

```bash
codex plugin list
```
Expected: agent-forge plugins (writing, prompts, msft-arch, pm) listed with version.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `.codex-plugin/` | Committed to repo; loaded by Codex CLI on session start |
| Agents | `.codex-plugin/agents/*.toml` | Exposed as Codex agents |
| Commands | `.codex-plugin/` | Available as Codex subcommands |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

Native alternative:
```bash
codex plugin update writing
codex plugin update --all
```

## Removing

```bash
agent-forge remove writing@codex-cli
# or native:
codex plugin remove writing
```

## Troubleshooting

**Plugin not appearing after install:**
1. Confirm `.codex-plugin/` exists in your working directory
2. Re-run `codex plugin marketplace add tqnonline/agent-forge` and retry install

**Skills not invoking:**
1. Check that `OPENAI_API_KEY` is set in your shell
2. Run `codex --version` to confirm you have a version that supports plugins

**See also:** [Contributing](../contributing/adding-a-plugin.md)
