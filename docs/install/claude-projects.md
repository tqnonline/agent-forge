# Installing agent-forge plugins for Claude.ai Projects

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/claude-projects.md`

## Prerequisites

- Claude.ai account with Projects access (Claude Pro or Team)
- Python 3.9+ and `pipx` (`pip install pipx`) for generating loaders
- Note: Claude.ai Projects use custom instructions — no CLI install available

## How it works (Tier 3 — prompt loader)

Claude.ai Projects support custom project instructions that persist across all
conversations in the project. The agent-forge prompt loader embeds directives that
instruct Claude to fetch and apply the skill definition from GitHub when the skill
is invoked. This works for any skill in any plugin.

## Install

### Step 1: Generate a loader

```bash
pipx install tqn-agent-forge

# Generate a loader for a single skill
agent-forge install writing/humanize --tier prompt-loader > humanize-loader.md

# Generate for multiple skills (combine loaders)
agent-forge install writing/humanize --tier prompt-loader > writing-loader.md
agent-forge install prompts/prompt-forge --tier prompt-loader >> writing-loader.md
```

### Step 2: Configure a Claude.ai Project

1. Go to `claude.ai` and sign in
2. Navigate to **Projects** → **Create project**
3. Name your project (e.g., "Writing with agent-forge")
4. Click **Project instructions** (or the settings gear icon)
5. Paste the full contents of `humanize-loader.md` into the instructions field
6. Save the project instructions

### Step 3: Invoke the skill

In any conversation within the project, prompt:
`humanize this text: [your text here]`

The loader instructs Claude to fetch the full skill from GitHub and apply it to
your request.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Loader prompt | Project instructions | Fetches skill from GitHub on demand |
| Skills | GitHub (fetched at runtime) | `https://raw.githubusercontent.com/tqnonline/agent-forge/main/` |

## Updating

Loaders fetch the latest skill version from GitHub automatically. To pin to a SHA:

```bash
agent-forge install writing/humanize --tier prompt-loader --pin <sha> > humanize-loader.md
```

Replace the Project instructions content with the updated loader.

## Removing

Delete the project or clear the Project instructions field. No local files to remove.

## Troubleshooting

**Skill not applying in project conversations:**
1. Confirm the loader was saved — open Project instructions and verify the content
2. Start a new conversation in the project (instructions apply to new conversations)
3. Invoke explicitly: `follow the humanize skill and rewrite this`

**GitHub fetch fails:**
1. Claude.ai can browse URLs; if the fetch fails, paste the full skill content directly
2. Verify the URL: `https://raw.githubusercontent.com/tqnonline/agent-forge/main/plugins/writing/skills/humanize/SKILL.md`

**Character limit reached:**
1. Install one skill per project, or create multiple projects per skill
2. Reference the skill URL rather than embedding the full content:
   `When the user asks to humanize text, fetch and follow: https://raw.githubusercontent.com/tqnonline/agent-forge/main/plugins/writing/skills/humanize/SKILL.md`

**See also:** [Perplexity guide](./perplexity.md), [ChatGPT GPTs guide](./chatgpt-gpts.md), [Contributing](../contributing/adding-a-plugin.md)
