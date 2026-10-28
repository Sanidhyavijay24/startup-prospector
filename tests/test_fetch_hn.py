"""
@file test_fetch_hn.py
@description Unit tests for Show HN parser and Algolia API client
"""

import pytest
from unittest.mock import patch, MagicMock
from fetch_hn import clean_project_name, fetch_show_hn_tools


def test_clean_project_name_variants():
    """Validates parser on varied Show HN title formats."""
    # Format with hyphen
    p1 = clean_project_name("Show HN: DevFlow - Fast terminal AI pair programmer")
    assert p1["name"] == "DevFlow"
    assert "Fast terminal AI" in p1["description"]

    # Format with colon
    p2 = clean_project_name("Show HN: AgentSmith: Autonomous web crawler in Rust")
    assert p2["name"] == "AgentSmith"
    assert "Autonomous web crawler" in p2["description"]

    # Format with em dash
    p3 = clean_project_name("Show HN: PromptPal — SQLite for prompts")
    assert p3["name"] == "PromptPal"
    assert "SQLite for prompts" in p3["description"]


def test_fetch_show_hn_tools_mock():
    """Mocking Algolia API response returns properly structured tools."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "hits": [
            {
                "title": "Show HN: CodeLens - Codebase visualization",
                "url": "https://codelens.dev",
                "author": "johndoe",
                "points": 45,
                "num_comments": 12,
                "objectID": "123456",
                "created_at": "2026-10-20T12:00:00Z",
            },
            {
                "title": "Ask HN: What is your favorite terminal?",
                "url": None,
                "author": "curious",
                "points": 50,
                "num_comments": 80,
                "objectID": "654321",
                "created_at": "2026-10-20T10:00:00Z",
            },
        ]
    }

    with patch("requests.get", return_value=mock_resp):
        tools = fetch_show_hn_tools(limit=5, min_points=5)
        # The 'Ask HN' should be filtered out
        assert len(tools) == 1
        assert tools[0]["name"] == "CodeLens"
        assert tools[0]["points"] == 45
        assert tools[0]["hn_author"] == "johndoe"
