"""Shared LLM judge for Layer B evals — uses Claude Sonnet 4.6 by default.

The judge is intentionally one tier above the invoked model (Haiku 4.5). Same-
model self-judging has documented bias (judge favors its own family's
patterns), and a judge can only catch errors at or below its own capability
ceiling. Override via `EVAL_JUDGE_MODEL` env var.

`temperature=0` is set on the judge call so the same (output, rubric) pair
scores identically across runs — required for the regression check to mean
anything.
"""

import json
import os
from pathlib import Path

import anthropic

JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "claude-sonnet-4-6")
BASELINE_FILE = Path(__file__).parent / "_baseline_scores.json"

JUDGE_PROMPT = """You are an expert evaluator. Score the following output against the rubric.

Input given to the skill:
---
{input}
---

Skill output:
---
{output}
---

Rubric (score 1-5 on each criterion):
---
{rubric}
---

Return ONLY a JSON object with shape:
{{"score": <average of all criteria, 1.0-5.0>, "reasoning": "<one sentence>"}}
"""


def score_against_rubric(
    output: str,
    rubric: str,
    case: dict,
    model: str = JUDGE_MODEL,
) -> float:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=400,
        temperature=0,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(
                input=case.get("input", ""),
                output=output,
                rubric=rubric,
            ),
        }],
    )
    text = message.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    parsed = json.loads(text)
    return float(parsed["score"])


def load_baseline(skill_path: str, case_id: str) -> float | None:
    if not BASELINE_FILE.exists():
        return None
    data = json.loads(BASELINE_FILE.read_text())
    return data.get(skill_path, {}).get(case_id)


def assert_no_regression(score: float, baseline: float | None, tolerance: float = 0.3) -> None:
    if baseline is None:
        return
    assert score >= baseline - tolerance, (
        f"Regression: score {score:.2f} < baseline {baseline:.2f} - tolerance {tolerance}"
    )


def update_baseline(skill_path: str, case_id: str, score: float) -> None:
    data = json.loads(BASELINE_FILE.read_text()) if BASELINE_FILE.exists() else {}
    data.setdefault(skill_path, {})[case_id] = round(score, 2)
    BASELINE_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
