# Installing agent-forge plugins for Cursor

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/cursor.md`

## Prerequisites

- Cursor installed (download from `cursor.com`)
- Cursor account (free or Pro)
- Optional: `agent-forge` Python CLI (`pipx install agent-forge`) for unified update tracking

## Quick install

### Option A: Cursor Marketplace (recommended)

1. Open Cursor
2. Go to `cursor.com/marketplace` or open Cursor → Extensions panel
3. Search for **"agent-forge"**
4. Click **Install**
5. Select which plugins to enable (writing, prompts, msft-arch, pm)

### Option B: Via the agent-forge CLI

```bash
pipx install agent-forge
agent-forge install writing --tier cursor
```

This copies skill artifacts into `.cursor-plugin/` and updates `.cursorrules`.

## Verify

Open Cursor → Settings → Extensions and confirm agent-forge appears in the installed list.

Alternatively, check that `.cursor-plugin/` exists in your project and `.cursorrules` references agent-forge skills.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Skills | `.cursor-plugin/` | Read by Cursor's AI context pipeline |
| Rules | `.cursorrules` | Instructs Cursor's AI to route to installed skills |
| Agents | `.cursor-plugin/agents/` | Available as Cursor agent modes |

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

For marketplace installs: Cursor → Extensions → agent-forge → Update.

## Removing

```bash
agent-forge remove writing@cursor
```

Or: Cursor → Extensions → agent-forge → Uninstall.

## Troubleshooting

**Plugin not appearing in Cursor Extensions:**
1. Ensure Cursor is updated to the latest version (Marketplace requires Cursor 0.40+)
2. Sign out and back into your Cursor account, then retry the install

**Skills not triggering in AI chat:**
1. Open `.cursorrules` and verify agent-forge routing rules are present
2. Try explicitly mentioning the skill: "use the humanize skill to rewrite this"

**See also:** [Contributing](../contributing/adding-a-plugin.md)
