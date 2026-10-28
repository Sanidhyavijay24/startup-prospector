"""
@file test_linter.py
@description Unit tests for outreach hook tone and syntax quality gate
"""

import pytest
from lint_hook import lint_hook_text, HookLintResult


def test_clean_hook_passes():
    """A natural, peer-to-peer 3-sentence hook with no buzzwords passes linting."""
    hook = (
        "Read your post from earlier this month introducing the new terminal diff engine. "
        "Giving engineers git-native review controls without forcing another heavy IDE extension solves the exact friction developers complain about. "
        "We are putting together an AI developer tooling benchmark and want to feature DevFlow AI."
    )
    result = lint_hook_text(hook)
    assert isinstance(result, HookLintResult)
    assert result.is_valid is True
    assert len(result.violations) == 0


def test_em_dash_fails():
    """Hooks containing em dashes (— or --) must be rejected immediately."""
    hook_unicode = (
        "Read your update on the new terminal diff engine—it solves the friction developers complain about. "
        "Would love to feature your tool in our upcoming dev benchmark."
    )
    result_unicode = lint_hook_text(hook_unicode)
    assert result_unicode.is_valid is False
    assert any("em dash" in v.lower() for v in result_unicode.violations)

    hook_ascii = (
        "Read your update on the new terminal diff engine -- it solves friction for developers. "
        "Would love to feature your tool in our upcoming dev benchmark."
    )
    result_ascii = lint_hook_text(hook_ascii)
    assert result_ascii.is_valid is False
    assert any("em dash" in v.lower() for v in result_ascii.violations)


def test_corporate_buzzwords_fail():
    """Hooks containing banned AI buzzwords must trigger violations."""
    banned_samples = [
        "Your new CLI engine is a game changer for terminal users. We would love to feature it.",
        "Let us delve into how you solved the git sync problem. We want to include you in our report.",
        "This release is a testament to your fast engineering cadence. We want to feature your tool.",
        "Your cutting-edge architecture caught our attention recently. Would love to feature your product.",
        "I hope this email finds you well after your recent release. We are putting together a benchmark.",
    ]
    for sample in banned_samples:
        result = lint_hook_text(sample)
        assert result.is_valid is False, f"Expected failure for: {sample}"
        assert any("buzzword" in v.lower() or "cliché" in v.lower() for v in result.violations)


def test_sentence_count_bounds():
    """Hooks must strictly contain between 2 and 3 sentences."""
    # 1 sentence (too short)
    too_short = "Your new terminal diff engine looks fast and solves git review friction."
    res_short = lint_hook_text(too_short)
    assert res_short.is_valid is False
    assert any("sentence count" in v.lower() for v in res_short.violations)

    # 5 sentences (too long)
    too_long = (
        "First sentence here about your product. "
        "Second sentence noting the architecture. "
        "Third sentence describing user experience. "
        "Fourth sentence asking for a call. "
        "Fifth sentence saying thanks."
    )
    res_long = lint_hook_text(too_long)
    assert res_long.is_valid is False
    assert any("sentence count" in v.lower() for v in res_long.violations)
