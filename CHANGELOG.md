# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Per-release detail lives under [`docs/releases/`](docs/releases/).

## [Unreleased]

## [1.0.1] — 2026-05-26

First release under the `tqnonline` GitHub organization.
See [release notes](docs/releases/v1.0.1.md).

### Changed
- Canonical home: `rahulnakmol/agent-forge` → `tqnonline/agent-forge`. All
  references in docs, code defaults (`manifest.py`, `cli.py`), badges, and
  raw-content links updated. GitHub permanent redirects keep v1.0.0 installs
  working.
- Classifier bumped to `Development Status :: 5 - Production/Stable`.

### Fixed
- `ci-structural.yml` and `ci-evals.yml` now install the `agent_forge` package
  before running tests. The workflows had been failing on test-collection
  errors since Phase 3 — unit tests import from `agent_forge`, but only the
  `tests` package was installed.

## [1.0.0] — 2026-05-03

First stable release. See [release notes](docs/releases/v1.0.0.md).

### Added
- **12 install targets:** 4 Tier 1a registry CLIs (Claude Code, GitHub Copilot
  CLI, Codex CLI, Cursor); 2 Tier 1b git-URL CLIs (Amp, Gemini CLI); 3 Tier 2
  copy-to-home adapters (Kilo Code, OpenCode, Crush); 3 Tier 3 prompt loaders
  (Perplexity, ChatGPT GPTs, Claude.ai Projects).
- **4 plugins / 46 skills:** `writing`, `prompts`, `msft-arch`, `pm`.
- **`agent-forge` Python CLI** (`pipx install agent-forge`) — `install`,
  `update`, `pin`, `remove`, `doctor`, plus 6 more commands across every
  supported tool.
- **974 unit tests** (Layer A — structural, no LLM calls).
- **230 eval tests** registered (Layer B — LLM-judged, requires
  `ANTHROPIC_API_KEY`).
- **9 Docker integration tests** (Layer C — `requires_docker` marker).
- **Agent-installable** — paste a single URL into any LLM agent and it follows
  the install guide without human intervention.

### Schemas frozen at v1.0
- `.claude-plugin/marketplace.json`
- `.github/plugin/marketplace.json`
- `.codex-plugin/marketplace.json`
- `.cursor-plugin/marketplace.json`
- Per-plugin `plugin.json`
- `~/.agent-forge/manifest.json` (`schema_version: 1`)
- `agent-forge` CLI command surface (11 commands)
- The install-URL pattern

Breaking changes to any of the above require a v2.0.0 major-version bump.

[Unreleased]: https://github.com/tqnonline/agent-forge/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/tqnonline/agent-forge/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/tqnonline/agent-forge/releases/tag/v1.0.0
