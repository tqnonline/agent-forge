# Installing agent-forge plugins for <TOOL NAME>

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/<filename>.md`

## Prerequisites

- <TOOL NAME> installed (`<install command for the tool itself>`)
- Optional: `agent-forge` Python CLI (`pipx install tqn-agent-forge`) for unified update tracking

## Quick install

### Option A: Native install command (recommended)

```bash
<TOOL NAME>'s native command for adding the agent-forge marketplace
```

### Option B: Via the agent-forge CLI

```bash
pipx install tqn-agent-forge   # or: uv tool install tqn-agent-forge
agent-forge install <plugin> --tier <tool-name>
```

## Verify

```bash
<command to list installed plugins/skills in the tool>
```
Expected: agent-forge plugins listed.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | <path> | Loaded on demand via frontmatter routing |
| Agents | <path> | <how this tool exposes agents> |
| Commands | <path> | <how this tool exposes slash commands> |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

Native alternative:
```bash
<tool's native update command, if any>
```

## Removing

```bash
agent-forge remove <plugin>@<tool-name>
```

## Troubleshooting

**Plugin not appearing after install:**
1. <Diagnostic step 1>
2. <Diagnostic step 2>

**See also:** [Loader pattern explainer](./loader-pattern.md), [Contributing](../contributing/adding-a-plugin.md)
