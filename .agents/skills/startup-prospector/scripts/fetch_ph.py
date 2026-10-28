"""
@file fetch_ph.py
@description Product Hunt weekly launched product reader via public Atom/RSS feed (Zero API key needed)
"""

import sys
import re
import json
import argparse
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import requests

PH_FEED_URL = "https://www.producthunt.com/feed"
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def parse_ph_title(raw_title: str) -> Dict[str, str]:
    """
    Parses 'AppName - Tagline' from Product Hunt feed title element.
    """
    parts = re.split(r"\s+[\-\–\—]\s+", raw_title.strip(), maxsplit=1)
    if len(parts) == 2:
        return {"name": parts[0].strip(), "tagline": parts[1].strip()}
    return {"name": raw_title.strip(), "tagline": raw_title.strip()}


def clean_html(raw_html: str) -> str:
    """Strips HTML tags and normalizes whitespace."""
    if not raw_html:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw_html)
    return " ".join(text.split()).strip()


def parse_ph_rss(xml_content: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Parses Product Hunt feed string (supporting both Atom <entry> and RSS <item> formats)
    into structured product dictionaries.
    """
    root = ET.fromstring(xml_content)
    results: List[Dict[str, Any]] = []

    # Check for Atom namespace
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    atom_entries = root.findall("atom:entry", ns)
    if not atom_entries:
        # Check without namespace
        atom_entries = root.findall(".//entry")

    if atom_entries:
        for entry in atom_entries:
            title = entry.findtext("atom:title", default="", namespaces=ns) or entry.findtext("title", default="")
            link_el = entry.find("atom:link", ns)
            if link_el is None:
                link_el = entry.find("link")
            link = link_el.get("href", "") if link_el is not None else ""
            pub_date = (
                entry.findtext("atom:published", default="", namespaces=ns)
                or entry.findtext("atom:updated", default="", namespaces=ns)
                or entry.findtext("published", default="")
            )
            content = (
                entry.findtext("atom:content", default="", namespaces=ns)
                or entry.findtext("atom:summary", default="", namespaces=ns)
                or entry.findtext("content", default="")
            )

            clean_desc = clean_html(content)
            parsed = parse_ph_title(title)

            results.append({
                "name": parsed["name"],
                "tagline": parsed["tagline"] if parsed["tagline"] != parsed["name"] else clean_desc[:80],
                "one_line_description": clean_desc if clean_desc else parsed["tagline"],
                "website": link,
                "ph_url": link,
                "published_at": pub_date,
                "category": "Product Hunt Launch",
            })

            if len(results) >= limit:
                break

        return results

    # Fallback to standard RSS <item>
    channel = root.find("channel")
    if channel is not None:
        for item in channel.findall("item"):
            raw_title = item.findtext("title") or ""
            link = item.findtext("link") or ""
            pub_date = item.findtext("pubDate") or ""
            desc = item.findtext("description") or ""

            clean_desc = clean_html(desc)
            parsed = parse_ph_title(raw_title)

            results.append({
                "name": parsed["name"],
                "tagline": parsed["tagline"],
                "one_line_description": clean_desc if clean_desc else parsed["tagline"],
                "website": link,
                "ph_url": link,
                "published_at": pub_date,
                "category": "Product Hunt Launch",
            })

            if len(results) >= limit:
                break

    return results


def fetch_product_hunt_weekly(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetches the latest trending products from Product Hunt's public feed.
    """
    headers = {"User-Agent": BROWSER_USER_AGENT}
    resp = requests.get(PH_FEED_URL, headers=headers, timeout=10)
    resp.raise_for_status()
    return parse_ph_rss(resp.text, limit=limit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch top launched products from Product Hunt RSS/Atom")
    parser.add_argument("--limit", type=int, default=10, help="Number of products to return (default 10)")
    parser.add_argument("--out", type=str, default=None, help="Optional output JSON path")

    args = parser.parse_args()
    products = fetch_product_hunt_weekly(limit=args.limit)

    formatted = json.dumps(products, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(formatted)
        print(f"Saved {len(products)} Product Hunt launches to {args.out}")
    else:
        print(formatted)
