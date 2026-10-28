"""
@file test_fetch_github.py
@description Unit tests for GitHub Star Velocity search and commit author email extractor
"""

import pytest
from unittest.mock import patch, MagicMock
from fetch_github import parse_commit_author, fetch_github_trending


def test_parse_commit_author_valid():
    """Extracts genuine developer name and email from git patch headers."""
    patch_sample = (
        "From a1b2c3d4e5f6 Mon Sep 17 00:00:00 2001\n"
        "From: Alex Mercer <alex@devflow.example.com>\n"
        "Date: Wed, 15 Oct 2026 12:00:00 +0000\n"
        "Subject: [PATCH] feat: implement terminal diff engine\n"
    )
    author = parse_commit_author(patch_sample)
    assert author is not None
    assert author["name"] == "Alex Mercer"
    assert author["email"] == "alex@devflow.example.com"


def test_parse_commit_author_filters_bots():
    """Discards GitHub bot and noreply emails to prevent spamming notification inboxes."""
    bot_samples = [
        "From: dependabot[bot] <dependabot[bot]@users.noreply.github.com>",
        "From: github-actions[bot] <github-actions[bot]@users.noreply.github.com>",
        "From: Jane Doe <12345678+janedoe@users.noreply.github.com>",
    ]
    for sample in bot_samples:
        author = parse_commit_author(sample)
        # Should return None or empty email for bot / noreply
        assert author is None or author.get("email") is None


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

    # Mock commit endpoint
    mock_commit_resp = MagicMock()
    mock_commit_resp.status_code = 200
    mock_commit_resp.text = "From: Alex Mercer <alex@tracecli.dev>\nDate: Wed, 15 Oct 2026"

    with patch("requests.get") as mock_get:
        mock_get.side_effect = [mock_search_resp, mock_commit_resp]
        results = fetch_github_trending(query="trace", min_stars=100, days=60, limit=5)
        assert len(results) == 1
        item = results[0]
        assert item["name"] == "trace-cli"
        assert item["website"] == "https://tracecli.dev"
        assert item["stars"] == 240
        assert item["founder_handle"] == "@alexmercer"
        assert item["founder_email"] == "alex@tracecli.dev"
