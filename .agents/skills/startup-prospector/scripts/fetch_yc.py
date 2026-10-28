"""
@file fetch_yc.py
@description Y Combinator batch discovery client via public Algolia search index (Zero API key needed)
"""

import sys
import re
import json
import argparse
from typing import List, Dict, Any, Optional, Tuple
import requests

YC_COMPANIES_URL = "https://www.ycombinator.com/companies"
DEFAULT_APP_ID = "45BWZJ1SGC"
# Fallback key valid through 2026+
DEFAULT_KEY = "ZDZlOGNhNWE0YzZhMGVhZDNkN2U5MDBlNmJjMGUzOGUxYjM3M2UzMjNlYTM5ZDdkZWQ0ZWQ4N2ZkMTIxNTVjMmFuYWx5dGljc1RhZ3M9eWNkYyZyZXN0cmljdEluZGljZXM9WUNDb21wYW55X3Byb2R1Y3Rpb24lMkNZQ0NvbXBhbnlfQnlfTGF1bmNoX0RhdGVfcHJvZHVjdGlvbiZ0YWdGaWx0ZXJzPSU1QiUyMnljZGNfcHVibGljJTIyJTVEJnZhbGlkVW50aWw9MTc5MzMxNzUzNQ=="
BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"

BATCH_MAPPINGS = {
    "S24": "Summer 2024",
    "W24": "Winter 2024",
    "S25": "Summer 2025",
    "W25": "Winter 2025",
    "S26": "Summer 2026",
    "W26": "Winter 2026",
    "S23": "Summer 2023",
    "W23": "Winter 2023",
}


def normalize_batch(batch_code: str) -> str:
    """Converts 'S24' or 'W24' to canonical 'Summer 2024' or 'Winter 2024'."""
    clean = batch_code.strip().upper()
    return BATCH_MAPPINGS.get(clean, batch_code.strip())


def get_live_yc_credentials() -> Tuple[str, str]:
    """
    Dynamically extracts the current public search credentials from YC's live companies page.
    Falls back to defaults if page layout shifts.
    """
    try:
        resp = requests.get(YC_COMPANIES_URL, headers={"User-Agent": BROWSER_USER_AGENT}, timeout=5)
        if resp.status_code == 200:
            match = re.search(r'window\.AlgoliaOpts\s*=\s*\{[^}]*"app":"([^"]+)"[^}]*"key":"([^"]+)"', resp.text)
            if match:
                return match.group(1), match.group(2)
    except Exception:
        pass
    return DEFAULT_APP_ID, DEFAULT_KEY


def fetch_yc_companies(
    batches: Optional[List[str]] = None,
    query: str = "",
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Queries active YC companies from recent batches via public Algolia index.
    Filters out inactive or acquired companies.
    """
    app_id, api_key = get_live_yc_credentials()
    algolia_url = f"https://{app_id.lower()}-dsn.algolia.net/1/indexes/YCCompany_production/query"

    headers = {
        "X-Algolia-Application-Id": app_id,
        "X-Algolia-API-Key": api_key,
        "Referer": "https://www.ycombinator.com/",
        "Content-Type": "application/json",
        "User-Agent": BROWSER_USER_AGENT,
    }

    payload: Dict[str, Any] = {
        "query": query,
        "hitsPerPage": min(limit * 3, 50),
    }

    if batches:
        expanded_batches = [f"batch:{normalize_batch(b)}" for b in batches]
        payload["facetFilters"] = [expanded_batches]

    resp = requests.post(algolia_url, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results: List[Dict[str, Any]] = []
    for hit in data.get("hits", []):
        status = hit.get("status") or "Active"
        # Strict filter: only live active companies
        if status.lower() != "active":
            continue

        name = hit.get("name", "")
        website = (hit.get("website") or "").strip()
        slug = hit.get("slug", "")
        yc_url = f"https://www.ycombinator.com/companies/{slug}" if slug else "https://www.ycombinator.com/companies"

        results.append({
            "name": name,
            "one_line_description": hit.get("one_liner") or hit.get("long_description") or "",
            "website": website if website else yc_url,
            "batch": hit.get("batch") or hit.get("batch_name") or "Unknown",
            "status": "Active",
            "team_size": hit.get("team_size"),
            "subindustry": hit.get("subindustry") or hit.get("industry") or "Technology",
            "country": hit.get("country") or "United States",
            "yc_profile_url": yc_url,
        })

        if len(results) >= limit:
            break

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query active Y Combinator batch companies")
    parser.add_argument("--batches", type=str, default="S24,W24", help="Comma-separated batch codes (e.g. 'S24,W24')")
    parser.add_argument("--query", type=str, default="ai", help="Search keyword (e.g. 'ai', 'developer', 'b2b')")
    parser.add_argument("--limit", type=int, default=10, help="Number of startups to return (default 10)")
    parser.add_argument("--out", type=str, default=None, help="Optional output JSON path")

    args = parser.parse_args()
    batch_list = [b.strip() for b in args.batches.split(",") if b.strip()]
    companies = fetch_yc_companies(batches=batch_list, query=args.query, limit=args.limit)

    formatted = json.dumps(companies, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(formatted)
        print(f"Saved {len(companies)} YC companies to {args.out}")
    else:
        print(formatted)
