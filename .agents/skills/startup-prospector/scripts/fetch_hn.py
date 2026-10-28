"""
@file fetch_hn.py
@description Free, rate-limit friendly startup discovery via Algolia Hacker News API
"""

import sys
import re
import json
import argparse
from typing import List, Dict, Any, Optional
import requests

HN_ALGOLIA_URL = "https://hn.algolia.com/api/v1/search_by_date"
HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"


def clean_project_name(raw_title: str) -> Dict[str, str]:
    """
    Parses 'Show HN: ProjectName - One line description' into clean name and description.
    """
    # Remove leading 'Show HN:' or 'Launch HN:'
    stripped = re.sub(r"^(?:Show|Launch)\s+HN:\s*", "", raw_title, flags=re.IGNORECASE).strip()

    # Split by colon, hyphen, or em-dash separator (e.g. 'Project: Description' or 'Project - Description')
    parts = re.split(r"(?:\s*:\s+|\s+[\-\–\—]\s+)", stripped, maxsplit=1)
    if len(parts) == 2:
        return {"name": parts[0].strip(), "description": parts[1].strip()}
    return {"name": stripped, "description": stripped}


def fetch_show_hn_tools(
    query: Optional[str] = None,
    limit: int = 15,
    min_points: int = 2,
) -> List[Dict[str, Any]]:
    """
    Fetches fresh developer tools and startup projects from Show HN.
    """
    params: Dict[str, Any] = {
        "tags": "show_hn",
        "hitsPerPage": min(limit * 2, 50),
    }

    url = HN_SEARCH_URL if query else HN_ALGOLIA_URL
    if query:
        params["query"] = query

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results: List[Dict[str, Any]] = []
    for hit in data.get("hits", []):
        points = hit.get("points") or 0
        if points < min_points:
            continue

        raw_title = hit.get("title", "")
        # Skip pure question / discussion posts
        if re.search(r"^(ask hn|tell hn)", raw_title, re.IGNORECASE):
            continue

        url = hit.get("url")
        object_id = hit.get("objectID")
        hn_url = f"https://news.ycombinator.com/item?id={object_id}"

        # If no external URL provided, the project is hosted/described in the HN thread
        target_url = url if url else hn_url

        parsed_name = clean_project_name(raw_title)

        results.append({
            "name": parsed_name["name"],
            "one_line_description": parsed_name["description"],
            "website": target_url,
            "hn_author": hit.get("author"),
            "points": points,
            "comments_count": hit.get("num_comments", 0),
            "created_at": hit.get("created_at"),
            "hn_discussion_url": hn_url,
        })

        if len(results) >= limit:
            break

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch fresh Show HN projects from Algolia API")
    parser.add_argument("--query", type=str, default=None, help="Optional search keyword (e.g. 'ai', 'cli', 'database')")
    parser.add_argument("--limit", type=int, default=10, help="Number of projects to return (default 10)")
    parser.add_argument("--min-points", type=int, default=2, help="Minimum upvotes threshold (default 2)")
    parser.add_argument("--out", type=str, default=None, help="Optional file path to save JSON output")

    args = parser.parse_args()
    tools = fetch_show_hn_tools(query=args.query, limit=args.limit, min_points=args.min_points)

    formatted_json = json.dumps(tools, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(formatted_json)
        print(f"Saved {len(tools)} Show HN tools to {args.out}")
    else:
        print(formatted_json)
