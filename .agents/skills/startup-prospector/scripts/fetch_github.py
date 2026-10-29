"""
@file fetch_github.py
@description GitHub Star Velocity search for breakout developer tools and public repositories
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
import requests

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
BROWSER_USER_AGENT = "Mozilla/5.0 (compatible; StartupProspector/1.0; +https://github.com/Sanidhyavijay24/startup-prospector)"


def get_github_headers() -> Dict[str, str]:
    """Builds headers, leveraging optional GITHUB_TOKEN if present in environment."""
    headers = {
        "User-Agent": BROWSER_USER_AGENT,
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def fetch_github_trending(
    query: str = "ai",
    days: int = 60,
    min_stars: int = 100,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Finds breakout repositories launched in the last N days with rapid star growth.
    Pulls canonical product website, public GitHub handle, and repo metrics.
    """
    cutoff_date = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    search_q = f"{query} created:>{cutoff_date} stars:>={min_stars}"

    params = {
        "q": search_q,
        "sort": "stars",
        "order": "desc",
        "per_page": min(limit * 2, 30),
    }

    headers = get_github_headers()
    resp = requests.get(GITHUB_SEARCH_URL, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results: List[Dict[str, Any]] = []
    items = data.get("items", [])

    for repo in items:
        name = repo.get("name", "")
        owner_login = repo.get("owner", {}).get("login", "")
        description = repo.get("description") or "Open-source developer tool"
        stars = repo.get("stargazers_count", 0)
        html_url = repo.get("html_url", "")
        homepage = (repo.get("homepage") or "").strip()

        # Canonical website preference: homepage if valid URL, else fallback to github repo
        website = homepage if (homepage.startswith("http://") or homepage.startswith("https://")) else html_url

        results.append({
            "name": name,
            "one_line_description": description,
            "website": website,
            "stars": stars,
            "created_at": repo.get("created_at"),
            "language": repo.get("language") or "Unknown",
            "founder_handle": f"@{owner_login}",
            "github_repo": html_url,
        })

        if len(results) >= limit:
            break

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find high-velocity breakout GitHub repositories")
    parser.add_argument("--query", type=str, default="ai", help="Search keyword (e.g. 'ai', 'agent', 'cli')")
    parser.add_argument("--days", type=int, default=60, help="Days lookback cutoff (default 60)")
    parser.add_argument("--min-stars", type=int, default=100, help="Minimum star threshold (default 100)")
    parser.add_argument("--limit", type=int, default=10, help="Number of repositories to return (default 10)")
    parser.add_argument("--out", type=str, default=None, help="Optional output JSON path")

    args = parser.parse_args()
    repos = fetch_github_trending(query=args.query, days=args.days, min_stars=args.min_stars, limit=args.limit)

    formatted = json.dumps(repos, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(formatted)
        print(f"Saved {len(repos)} GitHub repositories to {args.out}")
    else:
        print(formatted)
