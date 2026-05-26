# Contributing to agent-forge

Thank you for contributing to agent-forge! This guide covers everything you need
to get your contribution merged.

## Three contribution paths

| Path | When to use | Issue required? | Eval required? |
|---|---|---|---|
| Typo / bug fix | Fix a mistake in docs, frontmatter, or skill text | No | No |
| New skill | Add a skill to an existing plugin | Recommended | **Yes** |
| New plugin | Add a new plugin with one or more skills | **Yes (ADR discussion)** | **Yes** |

## DCO requirement

All commits must include a Developer Certificate of Origin sign-off. This is a
single-flag addition to your commit command:

```bash
git commit -s -m "your commit message"
```

The `-s` flag appends `Signed-off-by: Your Name <you@example.com>` to the commit
message. By signing off, you certify that you authored the contribution and have the
right to submit it under the project's BSD-3-Clause license. See
[ADR 0005](./docs/decisions/0005-dco-not-cla.md) for the rationale.

CI runs a DCO check on every PR. Commits without sign-off will block merge.

**Fixing a missing sign-off:**
```bash
git commit --amend -s
git push --force-with-lease
```

## Forking and branching

```bash
# Fork on GitHub, then:
gh repo fork tqnonline/agent-forge --clone --remote
cd agent-forge
git checkout -b <type>/<short-description>
# type: fix, feat, docs, chore
# examples: fix/humanize-voice-calibration, feat/writing-summarize-skill
```

## Typo or bug fix flow

For small fixes — typos, broken links, incorrect frontmatter, unclear instructions:

1. Fork and create a branch (see above)
2. Make your change
3. Run `pytest tests/unit -v` to confirm Layer A passes
4. Commit with DCO sign-off: `git commit -s -m "fix: correct typo in humanize description"`
5. Open a PR using the default template

No issue required. No eval suite required.

## New skill flow

A skill is a new capability added to an existing plugin. Follow these 7 steps:

1. **Fork and branch:** `git checkout -b feat/<plugin>-<skill-name>`

2. **Create the skill directory:**
   ```bash
   mkdir -p plugins/<plugin>/skills/<skill-name>
   ```

3. **Author `SKILL.md` with valid frontmatter:**
   ```yaml
   ---
   name: skill-name
   description: >
     Specific trigger conditions and use cases.
   license: BSD-3-Clause
   version: 1.0.0
   allowed-tools:
     - Read
   ---
   ```
   See [skill authoring guide](./docs/contributing/skill-authoring-guide.md) for full spec.

4. **Regenerate Tier 1a artifacts:**
   ```bash
   python scripts/regenerate-tier1-artifacts.py
   ```

5. **Write the eval suite** — required, no exceptions:
   ```bash
   mkdir -p tests/evals/<plugin>/<skill-name>
   # Create inputs.json and rubric.md
   ```
   See [adding a plugin](./docs/contributing/adding-a-plugin.md) for format details.

6. **Run Layer A tests:**
   ```bash
   .venv/bin/pytest tests/unit -v
   ```
   All must pass.

7. **Commit with DCO sign-off and open a PR:**
   ```bash
   git add plugins/<plugin>/skills/<skill-name>/ tests/evals/<plugin>/<skill-name>/
   git commit -s -m "feat(<plugin>): add <skill-name> skill"
   gh pr create --template .github/PULL_REQUEST_TEMPLATE/skill.md
   ```

## New plugin flow

A new plugin adds a new domain (e.g., a new industry vertical or tool suite).

**Before writing any code:** Open a GitHub Discussion to propose the plugin. Describe
the domain, the skills you plan to include, and why it belongs in agent-forge. A
maintainer will respond within one week. For significant architectural implications,
an ADR may be required — see [docs/decisions/](./docs/decisions/) for examples.

Once the discussion is approved, follow the same 7-step flow as a new skill, plus:

- Create `plugins/<name>/.claude-plugin/plugin.json`
- Create `plugins/<name>/THIRD_PARTY_NOTICES.md`
- Add the plugin to `.claude-plugin/marketplace.json`
- Run `python scripts/aggregate-notices.py` after adding `THIRD_PARTY_NOTICES.md`

Full details: [adding-a-plugin.md](./docs/contributing/adding-a-plugin.md).

## PR requirements

Before a PR can be merged, all of the following must be true:

- [ ] `pytest tests/unit -v` passes (Layer A — structural tests)
- [ ] DCO sign-off present on all commits (`Signed-off-by:` line)
- [ ] Eval suite present for any new skill (`inputs.json` + `rubric.md`)
- [ ] `python scripts/regenerate-tier1-artifacts.py --check` exits 0
- [ ] `python scripts/aggregate-notices.py --check` exits 0 (if THIRD_PARTY_NOTICES changed)
- [ ] `python scripts/build-install-index.py --check` exits 0 (if marketplace.json changed)
- [ ] PR uses the correct template from `.github/PULL_REQUEST_TEMPLATE/`

Layer B (LLM evals) runs automatically in CI and may fail if a skill quality regression
is detected. See [testing-locally.md](./docs/contributing/testing-locally.md) for how
to run evals locally.

## License attestation

By contributing to agent-forge, you agree that your contributions will be licensed
under the BSD-3-Clause license (see `LICENSE`). The DCO sign-off is your attestation
of this. If your contribution includes third-party content under a different license,
add it to `plugins/<name>/THIRD_PARTY_NOTICES.md`.

## Getting help

- **Questions:** Open a [GitHub Discussion](https://github.com/tqnonline/agent-forge/discussions)
- **Bugs:** Open a [GitHub Issue](https://github.com/tqnonline/agent-forge/issues)
- **Deeper guides:**
  - [Adding a plugin](./docs/contributing/adding-a-plugin.md)
  - [Skill authoring guide](./docs/contributing/skill-authoring-guide.md)
  - [Testing locally](./docs/contributing/testing-locally.md)
  - [Architecture decisions](./docs/decisions/)
