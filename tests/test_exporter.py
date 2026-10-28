"""
@file test_exporter.py
@description Unit tests for TSV and Excel exports
"""

import tempfile
from pathlib import Path
import pytest
from export_pipeline import generate_tsv_block, export_to_excel, validate_prospect_payload


def test_validate_prospect_payload(sample_valid_prospect):
    """Payload matching the schema passes Pydantic validation."""
    validated = validate_prospect_payload([sample_valid_prospect])
    assert len(validated) == 1
    assert validated[0].company.name == "DevFlow AI"


def test_generate_tsv_block(sample_valid_prospect):
    """Generates 4 tab-separated values for direct Google Sheets paste."""
    tsv = generate_tsv_block([sample_valid_prospect])
    lines = tsv.strip().split("\n")
    assert len(lines) == 1
    cols = lines[0].split("\t")
    # Expected: Hook A, Hook B, Hook Source, Best Channels
    assert len(cols) == 4
    assert "DevFlow AI" in cols[0]
    assert "diff engine" in cols[0]
    assert "https://devflow.example.com/blog" in cols[2]
    assert "Discord, LinkedIn, X (Twitter)" in cols[3]


def test_export_to_excel(sample_valid_prospect):
    """Generates a valid styled .xlsx file on disk."""
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir) / "prospects.xlsx"
        export_to_excel([sample_valid_prospect], str(out_path))
        assert out_path.exists()
        assert out_path.stat().st_size > 0
