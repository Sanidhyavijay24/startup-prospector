"""
@file test_hygiene.py
@description Unit tests for URL liveness, status codes, and Discord community checks
"""

import pytest
from unittest.mock import patch, MagicMock
from audit_hygiene import check_url_liveness, extract_discord_stats, HygieneAuditResult


def test_url_liveness_success():
    """Mocking a valid 200 OK response returns is_live=True."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.url = "https://example.com"
    mock_resp.text = "<html><head><title>Active SaaS</title></head><body>Welcome to the platform</body></html>"

    with patch("requests.get", return_value=mock_resp):
        res = check_url_liveness("https://example.com")
        assert isinstance(res, HygieneAuditResult)
        assert res.is_live is True
        assert res.status_code == 200
        assert res.is_parked is False


def test_url_liveness_404_failure():
    """Mocking a 404 response returns is_live=False."""
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.url = "https://example.com/dead"

    with patch("requests.get", return_value=mock_resp):
        res = check_url_liveness("https://example.com/dead")
        assert res.is_live is False
        assert res.status_code == 404


def test_parked_domain_detection():
    """Domains returning domain-for-sale or parked indicators are flagged."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.url = "https://example.com"
    mock_resp.text = "<html><body>This domain is for sale. Buy it on Sedo or GoDaddy.</body></html>"

    with patch("requests.get", return_value=mock_resp):
        res = check_url_liveness("https://example.com")
        assert res.is_live is False
        assert res.is_parked is True


def test_extract_discord_stats_success():
    """Mocking Discord public widget API returns member counts."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "guild": {"name": "DevFlow Community", "id": "12345"},
        "approximate_member_count": 1500,
        "approximate_presence_count": 320,
    }

    with patch("requests.get", return_value=mock_resp):
        stats = extract_discord_stats("https://discord.gg/devflow")
        assert stats is not None
        assert stats["member_count"] == 1500
        assert stats["online_count"] == 320
