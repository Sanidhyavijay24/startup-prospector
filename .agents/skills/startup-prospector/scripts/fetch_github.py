"""
@file fetch_github.py
@description GitHub Star Velocity search with commit author email extractor (Zero API key needed)
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional
import requests

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
BROWSER_USER_AGENT = "Mozilla/5.0 (compatible; StartupProspector/1.0; +https://github.com/Sanidhyavijay24/startup-prospector)"

BOT_EMAIL_PATTERN = re.compile(
    r"(?:\[bot\]|users\.noreply\.github\.com|actions@github\.com|dependabot|snyk-bot)",
    re.IGNORECASE
)


def parse_commit_author(patch_or_commit_text: str) -> Optional[Dict[str, str]]:
    """
    Extracts author name and email from git patch headers or commit metadata.
    Filters out bots and noreply privacy proxies.
    """
    match = re.search(r"^From:\s*([^<\n]+)<([^>\n]+)>", patch_or_commit_text, flags=re.MULTILINE)
    if not match:
        return None

    name = match.group(1).strip()
    email = match.group(2).strip()

    if BOT_EMAIL_PATTERN.search(name) or BOT_EMAIL_PATTERN.search(email):
        return None

    return {"name": name, "email": email}


def get_github_headers() -> Dict[str, str]:
    """Builds headers, leveraging GITHUB_TOKEN if present in environment."""
    headers = {
        "User-Agent": BROWSER_USER_AGENT,
        "Accept": "application/vnd.github.v3+json",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def fetch_commit_author(owner: str, repo: str, headers: Dict[str, str]) -> Optional[Dict[str, str]]:
    """
    Attempts to pull the top non-merge commit author directly from GitHub commits API
    or falls back to parsing patch text headers.
    """
    try:
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=5"
        resp = requests.get(commits_url, headers=headers, timeout=5)
        if resp.status_code != 200:
            return None

        # Check if response is patch text
        if "From:" in resp.text:
            parsed = parse_commit_author(resp.text)
            if parsed:
                return parsed

        # Otherwise parse JSON commits list
        commits_data = resp.json()
        if isinstance(commits_data, list):
            for c in commits_data:
                commit_obj = c.get("commit", {})
                author_info = commit_obj.get("author", {})
                name = author_info.get("name", "")
                email = author_info.get("email", "")

                if name and email and not BOT_EMAIL_PATTERN.search(email):
                    return {"name": name, "email": email}

    except Exception:
        pass

    return None


def fetch_github_trending(
    query: str = "ai",
    days: int = 60,
    min_stars: int = 100,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Finds breakout repositories launched in the last N days with rapid star growth.
    Extracts technical founder contact via commit author metadata.
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

        # Attempt commit author email extraction
        author = fetch_commit_author(owner_login, name, headers)

        results.append({
            "name": name,
            "one_line_description": description,
            "website": website,
            "stars": stars,
            "created_at": repo.get("created_at"),
            "language": repo.get("language") or "Unknown",
            "founder_handle": f"@{owner_login}",
            "founder_name": author.get("name") if author else None,
            "founder_email": author.get("email") if author else None,
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
