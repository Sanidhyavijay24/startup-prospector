"""
@file conftest.py
@description Pytest configuration, path setup, and shared fixtures
"""

import sys
from pathlib import Path
import pytest

# Ensure skill scripts directory is on sys.path
SKILL_SCRIPTS_PATH = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "startup-prospector" / "scripts"
if str(SKILL_SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SKILL_SCRIPTS_PATH))


@pytest.fixture
def sample_valid_prospect():
    """Fixture providing a verified, compliant startup prospect record."""
    return {
        "company": {
            "name": "DevFlow AI",
            "website": "https://devflow.example.com",
            "category": "Developer Tools",
            "one_line_description": "Git-native AI pair programming engine for terminal users.",
            "pricing_model": "Freemium",
            "launch_date": "2026-09-01",
            "status": "Active",
        },
        "founder": {
            "name": "Alex Mercer",
            "role": "Founder & CEO",
            "linkedin_url": "https://www.linkedin.com/in/alexmercer-dev/",
            "x_handle": "@alexmercer_ai",
            "work_email": "alex@devflow.example.com",
            "personal_email": None,
        },
        "community": {
            "discord_invite": "https://discord.gg/devflow",
            "slack_invite": None,
            "github_repo": "https://github.com/devflow-ai/cli",
            "discord_member_count": 1420,
        },
        "outreach": {
            "hook_a": "Read your post from earlier this month introducing the new terminal diff engine. Giving engineers git-native review controls without forcing another heavy IDE extension solves the exact friction developers complain about. We are putting together an AI developer tooling benchmark and want to feature DevFlow AI.",
            "hook_b": "DevFlow AI has stood out for keeping the CLI interaction instantaneous while other platforms overload their sidebars with complicated settings. For everyday refactoring, a lightweight terminal workflow beats enterprise GUI tools every time. Would love to feature DevFlow AI in our upcoming developer tools guide.",
            "hook_source": "https://devflow.example.com/blog",
            "best_channels": ["Discord", "LinkedIn", "X (Twitter)"],
        },
    }
