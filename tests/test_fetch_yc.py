"""
@file test_fetch_yc.py
@description Unit tests for Y Combinator batch discovery client
"""

import pytest
from unittest.mock import patch, MagicMock
from fetch_yc import fetch_yc_companies


def test_fetch_yc_companies_mock():
    """Mocks YC Algolia search response and verifies filtering of inactive companies."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "hits": [
            {
                "name": "SuperAgent AI",
                "batch_name": "Summer 2024",
                "website": "https://superagent.example.com",
                "one_liner": "Autonomous customer support agent with deterministic guardrails",
                "status": "Active",
                "team_size": 4,
                "subindustry": "Developer Tools",
                "slug": "superagent-ai",
                "country": "United States",
            },
            {
                "name": "DeadCo",
                "batch_name": "Summer 2024",
                "website": "https://deadco.example.com",
                "one_liner": "Crypto social network",
                "status": "Inactive",
                "team_size": 2,
                "subindustry": "Consumer",
                "slug": "deadco",
                "country": "United States",
            },
        ]
    }

    with patch("requests.post", return_value=mock_resp):
        results = fetch_yc_companies(batches=["S24"], query="agent", limit=5)
        # Inactive company DeadCo must be filtered out
        assert len(results) == 1
        co = results[0]
        assert co["name"] == "SuperAgent AI"
        assert co["batch"] == "Summer 2024"
        assert co["website"] == "https://superagent.example.com"
        assert co["status"] == "Active"
        assert "ycombinator.com/companies/superagent-ai" in co["yc_profile_url"]
