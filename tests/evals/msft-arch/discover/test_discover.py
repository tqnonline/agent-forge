"""tests/evals/msft-arch/discover/test_discover.py"""

import json
import pathlib

import pytest

SKILL_PATH = "msft-arch/discover"
HERE = pathlib.Path(__file__).parent
CASES = json.loads((HERE / "inputs.json").read_text())["cases"]
RUBRIC = (HERE / "rubric.md").read_text()


@pytest.mark.requires_anthropic_key
@pytest.mark.parametrize("case", CASES, ids=lambda c: c["id"])
def test_discover_quality(case, update_baselines) -> None:
    from evals._invoke import invoke_skill
    from evals._judge import (
        assert_no_regression,
        load_baseline,
        score_against_rubric,
        update_baseline,
    )
    skill_body = (
        HERE.parents[3] / "plugins/msft-arch/skills/discover/SKILL.md"
    ).read_text()
    output = invoke_skill(skill_body, case["input"], case.get("context"))
    score = score_against_rubric(output, RUBRIC, case)
    if update_baselines:
        update_baseline(SKILL_PATH, case["id"], score)
        return
    baseline = load_baseline(SKILL_PATH, case["id"])
    assert_no_regression(score, baseline)
