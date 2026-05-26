"""Eval-specific fixtures + CLI flag for baseline updates."""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--update-baselines", action="store_true", default=False,
        help="Update tests/evals/_baseline_scores.json with current scores",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "smoke: first parametrized case per skill — runs on PRs as a cheap subset",
    )


def pytest_collection_modifyitems(config, items):
    seen_files = set()
    for item in items:
        path = str(item.fspath)
        if path not in seen_files:
            item.add_marker(pytest.mark.smoke)
            seen_files.add(path)


@pytest.fixture
def update_baselines(request) -> bool:
    return request.config.getoption("--update-baselines")
