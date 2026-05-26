# Adding a plugin to agent-forge

This is the canonical 7-step flow for contributing a new plugin. A plugin is a
named collection of skills that serves a coherent domain (e.g., `writing`, `pm`).

Before starting: if you are adding a skill to an *existing* plugin, you only need
steps 3–7. Steps 1–2 are only required for a brand-new plugin.

## Step 1: Fork and clone

```bash
gh repo fork tqnonline/agent-forge --clone --remote
cd agent-forge
git checkout -b plugin/<your-plugin-name>
```

## Step 2: Create the plugin directory and manifest

```bash
mkdir -p plugins/<name>/skills
```

Create `plugins/<name>/.claude-plugin/plugin.json`:

```json
{
  "name": "<your-plugin-name>",
  "description": "One or two sentences describing what this plugin does",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "skills": "skills/"
}
```

**Rules:**
- `name` must be kebab-case, max 30 characters
- `description` must be a single paragraph, no bullet points
- `version` starts at `1.0.0` for new plugins

Also create `plugins/<name>/THIRD_PARTY_NOTICES.md` (can be empty if you have no
third-party dependencies):

```markdown
# Third-Party Notices for <name>

No third-party dependencies.
```

## Step 3: Author skills in `plugins/<name>/skills/<skill-name>/SKILL.md`

Each skill lives in its own subdirectory. The canonical format is Claude Code SKILL.md.

Minimum viable skill structure:
```
plugins/<name>/skills/<skill-name>/
  SKILL.md          ← required
  LICENSE.txt       ← required (BSD-3-Clause or compatible)
```

Full skill structure (for skills with supporting assets):
```
plugins/<name>/skills/<skill-name>/
  SKILL.md
  LICENSE.txt
  references/       ← reference documents the skill reads
  scripts/          ← helper scripts the skill may execute
  assets/           ← images, data files, etc.
```

**SKILL.md frontmatter spec:**

```yaml
---
name: skill-name          # kebab-case, matches directory name
description: >
  One or more sentences describing exactly when this skill should be invoked.
  Claude Code uses this to decide whether to route a user request here.
  Be specific: include trigger phrases and use cases.
license: BSD-3-Clause     # or "Complete terms in LICENSE.txt"
version: 1.0.0
allowed-tools:            # tools this skill is permitted to use
  - Read
  - Write
  - Edit
  - Grep
  - Glob
---

# Skill Title

[Skill body — full instructions for how the skill operates]
```

See the [skill authoring guide](./skill-authoring-guide.md) for detailed guidance.

## Step 4: Run the artifact regenerator

All Tier 1a CLIs (Claude Code, GitHub Copilot CLI, Codex CLI, Cursor) require
committed artifacts derived from the canonical skill files. After adding or modifying
skills, always run:

```bash
python scripts/regenerate-tier1-artifacts.py
```

This updates `.claude-plugin/`, `.github/plugin/`, `.codex-plugin/`, and
`.cursor-plugin/` from the canonical `plugins/` source.

Verify no drift:
```bash
python scripts/regenerate-tier1-artifacts.py --check
```

## Step 5: Write an eval suite

Every skill **must** have an eval suite before it can be merged. Create:

```
tests/evals/<plugin-name>/<skill-name>/
  inputs.json       ← required
  rubric.md         ← required
```

**`inputs.json` format:**
```json
[
  {
    "id": "basic-humanize",
    "description": "Standard humanize request",
    "user_message": "Humanize this text: The utilization of advanced methodologies...",
    "expected_behavior": "Returns natural human prose without AI patterns"
  }
]
```

**`rubric.md` format:**
```markdown
# Eval Rubric: <skill-name>

## Criteria

| Criterion | Weight | Pass condition |
|---|---|---|
| Removes AI patterns | 30% | No instances of "utilize", "leverage", "delve" |
| Voice consistency | 40% | Matches requested regional voice shortcode |
| Readability | 30% | Flesch-Kincaid score ≥ 60 |

## Scoring

- Pass: all criteria met or weighted average ≥ 0.8
- Fail: any criterion below 0.5
```

## Step 6: Run the test suite

```bash
# Layer A — structural tests, always required, no API key needed
.venv/bin/pytest tests/unit -v

# Layer B — eval tests, requires ANTHROPIC_API_KEY
export ANTHROPIC_API_KEY=sk-ant-...
.venv/bin/pytest tests/evals/<plugin-name>/<skill-name> -v
```

All Layer A tests must pass before you open a PR. Layer B is run by CI.

See [testing-locally.md](./testing-locally.md) for full details.

## Step 7: Submit a PR with DCO sign-off

```bash
git add plugins/<name>/ tests/evals/<name>/
git commit -s -m "feat(plugins): add <name> plugin"
# The -s flag adds the DCO Signed-off-by line
git push origin plugin/<your-plugin-name>
gh pr create --template .github/PULL_REQUEST_TEMPLATE/plugin.md
```

**PR checklist:**
- [ ] `plugins/<name>/.claude-plugin/plugin.json` present and valid
- [ ] All SKILL.md files have required frontmatter fields
- [ ] `tests/evals/<name>/<skill-name>/inputs.json` and `rubric.md` present
- [ ] `python scripts/regenerate-tier1-artifacts.py --check` exits 0
- [ ] `pytest tests/unit -v` passes
- [ ] `THIRD_PARTY_NOTICES.md` updated if any dependencies added
- [ ] Commits signed off with `git commit -s`

## Register in the marketplace

If this is a new plugin, also add it to `.claude-plugin/marketplace.json`:

```json
{
  "name": "<your-plugin-name>",
  "description": "Same as plugin.json description",
  "source": "./plugins/<your-plugin-name>"
}
```

Then re-run `python scripts/regenerate-tier1-artifacts.py` and include the
updated marketplace files in your PR.
