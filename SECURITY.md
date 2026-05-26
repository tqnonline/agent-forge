# Security Policy

## Reporting a Vulnerability

Please report security vulnerabilities via [GitHub Security Advisories](https://github.com/tqnonline/agent-forge/security/advisories/new)
or by emailing **rahulnakmol@gmail.com** with the subject line `SECURITY: agent-forge`.

Do **not** open public issues for security reports.

## Supported Versions

Until v1.0.0, only the latest tagged release receives security fixes.

After v1.0.0, the latest minor release on the current major version receives
security fixes for at least 6 months following the next release.

## Scope

In scope:
- The `agent-forge` Python CLI (`scripts/agent_forge/`)
- The install scripts (`scripts/install-*.sh`)
- The translator implementations (`scripts/agent_forge/translators/`)

Out of scope:
- Third-party CLI behavior (Claude Code, Copilot CLI, Codex, etc.) — report to the upstream vendor
- Skill content provided by community contributors — report to the plugin owner via CODEOWNERS
