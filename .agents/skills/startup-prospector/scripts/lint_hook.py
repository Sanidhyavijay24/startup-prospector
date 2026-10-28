"""
@file lint_hook.py
@description Deterministic quality gate for outreach hook tone, punctuation, and syntax
"""

import sys
import re
from typing import List
from pydantic import BaseModel, Field

# Disallowed AI clichés, hyperbole, and spammy openers
BANNED_BUZZWORDS = [
    r"\bgame[ -]?changer\b",
    r"\bdelve\b",
    r"\btestament\b",
    r"\bcutting[ -]?edge\b",
    r"\brevolutionary\b",
    r"\bspearhead\b",
    r"\bunleash\b",
    r"\belevate\b",
    r"\bhope this (email )?finds you well\b",
    r"\bin today'?s fast[- ]paced world\b",
    r"\bnavigating the( modern)? landscape\b",
    r"\bi came across your (profile|product)\b",
]


class HookLintResult(BaseModel):
    """Result schema for hook validation."""
    is_valid: bool
    violations: List[str] = Field(default_factory=list)
    sentence_count: int = 0
    word_count: int = 0


def count_sentences(text: str) -> int:
    """Split text into sentences using punctuation boundaries."""
    # Split on periods, exclamation marks, question marks followed by space or end of string
    cleaned = text.strip()
    if not cleaned:
        return 0
    sentences = re.split(r"[.!?]+(?:\s+|$)", cleaned)
    # Filter empty items
    return len([s for s in sentences if s.strip()])


def lint_hook_text(text: str) -> HookLintResult:
    """
    Validates hook text against strict tone and syntax criteria.
    - No em dashes (— or --)
    - No AI clichés or corporate buzzwords
    - Strictly between 2 and 3 sentences
    """
    violations: List[str] = []
    cleaned = text.strip()

    # Rule 1: No Em Dashes
    if "—" in cleaned or "--" in cleaned:
        violations.append("Em dash detected ('—' or '--'). Use standard commas or periods.")

    # Rule 2: Corporate Buzzwords & Clichés
    for pattern in BANNED_BUZZWORDS:
        match = re.search(pattern, cleaned, re.IGNORECASE)
        if match:
            violations.append(f"Banned buzzword or cliché detected: '{match.group(0)}'.")

    # Rule 3: Sentence Count (Strictly 2 to 3 sentences)
    s_count = count_sentences(cleaned)
    if s_count < 2 or s_count > 3:
        violations.append(
            f"Sentence count violation: Found {s_count} sentences. Expected strictly 2 to 3 sentences."
        )

    # Word count check
    words = cleaned.split()
    w_count = len(words)
    if w_count < 20:
        violations.append(f"Hook too short: {w_count} words. Must be between 25 and 85 words.")
    elif w_count > 90:
        violations.append(f"Hook too long: {w_count} words. Must be between 25 and 85 words.")

    return HookLintResult(
        is_valid=len(violations) == 0,
        violations=violations,
        sentence_count=s_count,
        word_count=w_count,
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lint_hook.py \"<hook text>\"")
        sys.exit(1)

    raw_text = " ".join(sys.argv[1:])
    result = lint_hook_text(raw_text)
    print(result.model_dump_json(indent=2))
    sys.exit(0 if result.is_valid else 1)
