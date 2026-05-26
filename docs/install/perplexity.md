# Installing agent-forge plugins for Perplexity Spaces

> **Agent-installable:** This guide is written so an LLM agent can read it and
> execute the install commands directly. Paste this URL into your agent:
> `https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/perplexity.md`

## Prerequisites

- Perplexity account with Spaces access (`perplexity.ai`)
- Python 3.9+ and `pipx` (`pip install pipx`) for generating loaders
- Note: Perplexity has no CLI or file-based install mechanism — skills are loaded via prompt loaders

## How it works (Tier 3 — prompt loader)

Perplexity Spaces uses custom instructions to configure an AI persona. The agent-forge
prompt loader technique embeds instructions that tell Perplexity to fetch the skill
definition from GitHub when the skill is invoked. This gives full skill functionality
without a native install.

## Install

### Step 1: Generate a loader for the skill(s) you want

```bash
pipx install tqn-agent-forge

# Generate a loader for a single skill
agent-forge install writing/humanize --tier prompt-loader > humanize-loader.md

# Generate loaders for multiple skills
agent-forge install prompts/prompt-forge --tier prompt-loader > prompt-forge-loader.md
```

### Step 2: Configure a Perplexity Space

1. Go to `perplexity.ai` and sign in
2. Navigate to **Spaces** → **Create Space**
3. Name your space (e.g., "Writing Assistant")
4. Open the **Custom Instructions** panel
5. Paste the entire contents of `humanize-loader.md` into the instructions field
6. Save the space

### Step 3: Invoke the skill

In the Space, prompt: `humanize this text: [your text here]`

The loader instructs Perplexity to fetch the full skill definition from GitHub and
apply it to your request.

## What gets installed

| Item | Where it lands | Notes |
|---|---|---|
| Loader prompt | Perplexity Space custom instructions | Fetches skill from GitHub on demand |
| Skills | GitHub (fetched at runtime) | `https://raw.githubusercontent.com/tqnonline/agent-forge/main/` |

## Updating

Loaders always fetch the latest skill version from GitHub. No update step is needed
unless you want to pin to a specific SHA:

```bash
agent-forge install writing/humanize --tier prompt-loader --pin <sha> > humanize-loader.md
```

Repaste the updated loader into your Space's custom instructions.

## Removing

Delete or edit the Space in Perplexity to remove the skill. No files to clean up locally.

## Troubleshooting

**Skill not activating after pasting loader:**
1. Confirm the full loader content was pasted — truncated instructions break the fetch directive
2. Try explicitly triggering: `activate humanize skill and rewrite this paragraph`

**Fetch fails (network or 404):**
1. Verify the skill exists: `https://raw.githubusercontent.com/tqnonline/agent-forge/main/plugins/writing/skills/humanize/SKILL.md`
2. Regenerate the loader with `agent-forge install writing/humanize --tier prompt-loader`

**See also:** [ChatGPT GPTs guide](./chatgpt-gpts.md), [Claude.ai Projects guide](./claude-projects.md), [Contributing](../contributing/adding-a-plugin.md)
