"""
@file test_fetch_github.py
@description Unit tests for GitHub Star Velocity search
"""

import pytest
from unittest.mock import patch, MagicMock
from fetch_github import fetch_github_trending


def test_fetch_github_trending_mock():
    """Mocks GitHub Search API and verifies extracted repository fields."""
    mock_search_resp = MagicMock()
    mock_search_resp.status_code = 200
    mock_search_resp.json.return_value = {
        "items": [
            {
                "name": "trace-cli",
                "full_name": "alexmercer/trace-cli",
                "description": "Terminal-native distributed trace viewer for AI microservices",
                "html_url": "https://github.com/alexmercer/trace-cli",
                "homepage": "https://tracecli.dev",
                "stargazers_count": 240,
                "created_at": "2026-09-01T10:00:00Z",
                "language": "Rust",
                "owner": {"login": "alexmercer"},
            }
        ]
    }

    with patch("requests.get", return_value=mock_search_resp):
        results = fetch_github_trending(query="trace", min_stars=100, days=60, limit=5)
        assert len(results) == 1
        item = results[0]
        assert item["name"] == "trace-cli"
        assert item["website"] == "https://tracecli.dev"
        assert item["stars"] == 240
        assert item["founder_handle"] == "@alexmercer"
        assert item["github_repo"] == "https://github.com/alexmercer/trace-cli"
