# Installing agent-forge plugins for GitHub Copilot CLI

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/github-copilot-cli.md`

## Prerequisites

- GitHub Copilot CLI installed (`npm install -g @githubnext/github-copilot-cli`)
- GitHub account with active Copilot subscription
- Optional: `agent-forge` Python CLI (`pipx install agent-forge`) for unified update tracking

## Quick install

### Option A: Native install command (recommended)

```bash
# Register the agent-forge plugin marketplace
copilot plugin marketplace add tqnonline/agent-forge

# Install individual plugins
copilot plugin install writing
copilot plugin install prompts
copilot plugin install msft-arch
copilot plugin install pm
```

### Option B: Via the agent-forge CLI

```bash
pipx install agent-forge
agent-forge install writing --tier github-copilot-cli
```

## Verify

```bash
copilot plugin list
```
Expected: agent-forge plugins listed with their skill counts and install path.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `.github/plugin/` | Committed to repo; picked up by Copilot CLI plugin framework |
| Agents | `.github/plugin/agents/*.agent.md` | Exposed as Copilot agents |
| Commands | Via Copilot CLI plugin framework | Available as `copilot` subcommands after install |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

Native alternative:
```bash
copilot plugin update writing
```

## Removing

```bash
agent-forge remove writing@github-copilot-cli
# or native:
copilot plugin remove writing
```

## Troubleshooting

**Plugin not appearing after install:**
1. Confirm `.github/plugin/` exists in your repository root
2. Run `copilot plugin list` — if missing, re-run the marketplace add command

**Authentication errors:**
1. Run `gh auth login` and verify Copilot is enabled on your account
2. Check `copilot plugin --help` for current auth requirements

**See also:** [Contributing](../contributing/adding-a-plugin.md)
