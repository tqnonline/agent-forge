# agent-forge

A curated, BSD-3-Clause marketplace of agent skills, plugins, and slash commands.
Works natively with Claude Code, GitHub Copilot CLI, OpenAI Codex CLI, and Cursor.
Git-URL install for Amp and Gemini CLI. Copy-to-home adapters for Kilo Code,
OpenCode, and Crush. Portable prompt loaders for Perplexity, ChatGPT GPTs,
and Claude.ai Projects.

**12 install targets. 4 plugins. 46 skills. One canonical source.**

## 30-second install

**Claude Code:**
```bash
claude plugin marketplace add github:tqnonline/agent-forge
claude plugin install writing
```

**GitHub Copilot CLI:**
```bash
copilot plugin marketplace add tqnonline/agent-forge
```

**Codex CLI:**
```bash
codex plugin marketplace add tqnonline/agent-forge
```

**Cursor:** Open `cursor.com/marketplace`, search "agent-forge", click Install.

**Amp:**
```bash
amp skill add github:tqnonline/agent-forge
```

**Gemini CLI:**
```bash
gemini skills install github:tqnonline/agent-forge
```

**Kilo Code, OpenCode, or Crush:**
```bash
pipx install tqn-agent-forge   # or: uv tool install tqn-agent-forge
agent-forge install writing --tier kilocode   # or opencode, or crush
```

**Perplexity, ChatGPT GPTs, Claude.ai Projects:** See [docs/install/_index.md](./docs/install/_index.md) — these use prompt loaders rather than native install.

## What's in the marketplace

| Plugin | Skills | Description |
|---|---|---|
| `writing` | humanize | Detect AI writing patterns and rewrite in natural human voice |
| `prompts` | prompt-forge | Interactive prompt engineering via structured dialogue |
| `msft-arch` | 32 skills | Microsoft enterprise architecture: Azure, M365, Power Platform, Dynamics 365 |
| `pm` | 12 skills | Product/Program Management: PRD generation, epic decomposition, 11-Star review |

## Telling an agent to install

Paste this into any LLM agent:

> Install agent-forge plugins from  
> https://raw.githubusercontent.com/tqnonline/agent-forge/main/docs/install/_index.md

The agent fetches the catalog, identifies your tool, and runs the correct install commands.

## Updating

```bash
agent-forge update --check    # see what's stale
agent-forge update            # apply
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Three paths: typo fix (no issue needed),
new skill (must include eval suite), new plugin (requires ADR discussion). DCO sign-off
required (`git commit -s`).

## License

BSD-3-Clause. Per-plugin assets may carry their own licenses; see `THIRD_PARTY_NOTICES.md`.
