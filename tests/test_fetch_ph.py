"""
@file test_fetch_ph.py
@description Unit tests for Product Hunt RSS feed parser
"""

import pytest
from unittest.mock import patch, MagicMock
from fetch_ph import parse_ph_rss, fetch_product_hunt_weekly

SAMPLE_PH_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Product Hunt</title>
    <link>https://www.producthunt.com</link>
    <description>The best new products, every day</description>
    <item>
      <title>Krea 2.0 - Real-time AI video generation</title>
      <link>https://www.producthunt.com/posts/krea-2-0</link>
      <pubDate>Mon, 20 Oct 2026 07:00:00 +0000</pubDate>
      <description>&lt;p&gt;Generate video in real-time with next-gen diffusion.&lt;/p&gt;</description>
    </item>
    <item>
      <title>TabNine CLI - AI code completion in your terminal</title>
      <link>https://www.producthunt.com/posts/tabnine-cli</link>
      <pubDate>Sun, 19 Oct 2026 07:00:00 +0000</pubDate>
      <description>&lt;p&gt;Context-aware code completion for bash and zsh.&lt;/p&gt;</description>
    </item>
  </channel>
</rss>
"""


def test_parse_ph_rss():
    """Parses XML RSS feed into structured product records."""
    products = parse_ph_rss(SAMPLE_PH_RSS, limit=5)
    assert len(products) == 2
    p1 = products[0]
    assert p1["name"] == "Krea 2.0"
    assert "Real-time AI video generation" in p1["tagline"]
    assert p1["ph_url"] == "https://www.producthunt.com/posts/krea-2-0"

    p2 = products[1]
    assert p2["name"] == "TabNine CLI"
    assert "AI code completion" in p2["tagline"]


def test_fetch_product_hunt_weekly_mock():
    """Mocks network request to Product Hunt feed endpoint."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.text = SAMPLE_PH_RSS

    with patch("requests.get", return_value=mock_resp):
        results = fetch_product_hunt_weekly(limit=1)
        assert len(results) == 1
        assert results[0]["name"] == "Krea 2.0"
