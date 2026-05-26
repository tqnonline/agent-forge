"""tests/unit/test_github.py"""

from unittest.mock import patch, MagicMock

from agent_forge.github import resolve_plugin_sha, raw_url


def test_raw_url() -> None:
    url = raw_url("tqnonline/agent-forge", "main", "plugins/writing/skills/humanize/SKILL.md")
    assert url == "https://raw.githubusercontent.com/tqnonline/agent-forge/main/plugins/writing/skills/humanize/SKILL.md"


def test_resolve_plugin_sha_uses_commits_api() -> None:
    fake_response = MagicMock()
    fake_response.json.return_value = [{"sha": "abc123"}]
    fake_response.raise_for_status = MagicMock()
    with patch("httpx.get", return_value=fake_response) as mock_get:
        sha = resolve_plugin_sha("tqnonline/agent-forge", "main", "plugins/writing")
        assert sha == "abc123"
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "/commits" in args[0]
        assert kwargs["params"]["path"] == "plugins/writing"
        assert kwargs["params"]["sha"] == "main"
