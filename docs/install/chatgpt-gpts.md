# Installing agent-forge plugins for ChatGPT custom GPTs

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/chatgpt-gpts.md`

## Prerequisites

- ChatGPT account with GPT Builder access (ChatGPT Plus, Team, or Enterprise)
- Python 3.9+ and `pipx` (`pip install pipx`) for generating loaders
- Note: Custom GPTs have no CLI install — skills are loaded via prompt loaders in the Instructions field

## How it works (Tier 3 — prompt loader)

Custom GPTs use an "Instructions" field to define behavior. The agent-forge prompt
loader embeds a directive that instructs the GPT to fetch the skill definition from
GitHub when the skill name is invoked. The fetched content guides the GPT's response.

## Install

### Step 1: Generate a loader

```bash
pipx install agent-forge

# Generate a loader for a single skill
agent-forge install writing/humanize --tier prompt-loader > humanize-loader.md

# Generate for the full writing plugin
agent-forge install prompts/prompt-forge --tier prompt-loader > prompt-forge-loader.md
```

### Step 2: Create or configure a custom GPT

1. Go to `chatgpt.com` → **Explore GPTs** → **Create**
2. Switch to the **Configure** tab
3. Set a name and description for your GPT (e.g., "Humanize Writing Assistant")
4. In the **Instructions** field, paste the full contents of `humanize-loader.md`
5. Optionally enable **Web browsing** to allow the GPT to fetch skill updates
6. Click **Save** and set visibility

### Step 3: Invoke the skill

Open your custom GPT and prompt: `humanize this text: [your text here]`

The loader instructs the GPT to fetch the full skill definition from GitHub and apply it.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Loader prompt | GPT Instructions field | Fetches skill from GitHub on demand |
| Skills | GitHub (fetched at runtime) | `https://raw.githubusercontent.com/tqnonline/agent-forge/main/` |

## Updating

Loaders always fetch the latest version from GitHub. To pin to a SHA:

```bash
agent-forge install writing/humanize --tier prompt-loader --pin <sha> > humanize-loader.md
```

Paste the updated loader into your GPT's Instructions field and save.

## Removing

Delete the custom GPT or replace the Instructions field content. No local files to clean up.

## Troubleshooting

**GPT not following the skill instructions:**
1. Verify the full loader was pasted — check for truncation at the character limit
2. Enable "Web browsing" in the GPT's capabilities so it can fetch the skill definition
3. Try a more explicit invocation: `follow the humanize skill instructions and rewrite this`

**Skill fetch returns 404:**
1. Verify the raw URL is reachable: `https://raw.githubusercontent.com/tqnonline/agent-forge/main/plugins/writing/skills/humanize/SKILL.md`
2. Regenerate the loader: `agent-forge install writing/humanize --tier prompt-loader`

**See also:** [Perplexity guide](./perplexity.md), [Claude.ai Projects guide](./claude-projects.md), [Contributing](../contributing/adding-a-plugin.md)
