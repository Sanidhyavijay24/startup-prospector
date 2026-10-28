"""
@file audit_hygiene.py
@description Hygiene auditor for URL liveness, parking page detection, and Discord community stats
"""

import sys
import re
from typing import Optional, Dict, Any
import requests
from pydantic import BaseModel, Field

BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

PARKED_INDICATORS = [
    r"domain is for sale",
    r"buy this domain",
    r"parked free",
    r"sedo domain parking",
    r"godaddy parked",
    r"hugedomains\.com",
    r"dan\.com",
    r"afternic\.com",
]


class HygieneAuditResult(BaseModel):
    """Hygiene audit findings for a target URL."""
    url: str
    is_live: bool
    status_code: Optional[int] = None
    final_url: Optional[str] = None
    is_parked: bool = False
    error: Optional[str] = None


def check_url_liveness(url: str, timeout: int = 8) -> HygieneAuditResult:
    """
    Sends an HTTP GET request with a browser User-Agent to verify live status.
    Flags 404s, DNS failures, SSL expired certs, and parked domains.
    """
    headers = {"User-Agent": BROWSER_USER_AGENT}
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        final_url = str(resp.url)
        status_code = resp.status_code

        # Check for HTTP success
        if status_code < 200 or status_code >= 400:
            return HygieneAuditResult(
                url=url,
                is_live=False,
                status_code=status_code,
                final_url=final_url,
                error=f"HTTP status {status_code}",
            )

        # Check for parked domain markers in page body
        body_text = resp.text[:10000].lower()
        is_parked = any(re.search(pattern, body_text) for pattern in PARKED_INDICATORS)
        if is_parked:
            return HygieneAuditResult(
                url=url,
                is_live=False,
                status_code=status_code,
                final_url=final_url,
                is_parked=True,
                error="Domain parking / sale page detected",
            )

        return HygieneAuditResult(
            url=url,
            is_live=True,
            status_code=status_code,
            final_url=final_url,
            is_parked=False,
        )

    except requests.exceptions.SSLError as err:
        return HygieneAuditResult(url=url, is_live=False, error=f"SSL Error: {err}")
    except requests.exceptions.ConnectionError as err:
        return HygieneAuditResult(url=url, is_live=False, error=f"Connection Error: {err}")
    except requests.exceptions.Timeout:
        return HygieneAuditResult(url=url, is_live=False, error="Request Timeout (>8s)")
    except Exception as err:
        return HygieneAuditResult(url=url, is_live=False, error=str(err))


def extract_discord_stats(invite_url: str) -> Optional[Dict[str, Any]]:
    """
    Extracts live community stats via Discord's public widget API.
    Does not require a Discord bot token or login.
    """
    match = re.search(r"(?:discord\.gg|discord\.com/invite)/([a-zA-Z0-9\-]+)", invite_url)
    if not match:
        return None

    code = match.group(1)
    api_url = f"https://discord.com/api/v8/invites/{code}?with_counts=true"

    try:
        resp = requests.get(api_url, headers={"User-Agent": BROWSER_USER_AGENT}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "guild_name": data.get("guild", {}).get("name"),
                "member_count": data.get("approximate_member_count", 0),
                "online_count": data.get("approximate_presence_count", 0),
            }
    except Exception:
        pass

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audit_hygiene.py <url>")
        sys.exit(1)

    target_url = sys.argv[1]
    result = check_url_liveness(target_url)
    print(result.model_dump_json(indent=2))
    sys.exit(0 if result.is_live else 1)
