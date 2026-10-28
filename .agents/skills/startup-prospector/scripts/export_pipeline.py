"""
@file export_pipeline.py
@description Formats and exports enriched startup prospects to styled Excel (.xlsx) and 1-click TSV
"""

import sys
import json
from pathlib import Path
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


class Company(BaseModel):
    name: str
    website: str
    category: str
    one_line_description: str
    pricing_model: Optional[str] = "Freemium"
    launch_date: Optional[str] = None
    status: str = "Active"


class Founder(BaseModel):
    name: str
    role: str = "Founder & CEO"
    linkedin_url: Optional[str] = None
    x_handle: Optional[str] = None
    work_email: Optional[str] = None
    personal_email: Optional[str] = None


class Community(BaseModel):
    discord_invite: Optional[str] = None
    slack_invite: Optional[str] = None
    github_repo: Optional[str] = None
    discord_member_count: Optional[int] = None


class Outreach(BaseModel):
    hook_a: str
    hook_b: str
    hook_source: str
    best_channels: List[str] = Field(default_factory=list)


class StartupProspect(BaseModel):
    company: Company
    founder: Founder
    community: Community
    outreach: Outreach


def validate_prospect_payload(raw_list: List[Dict[str, Any]]) -> List[StartupProspect]:
    """Validates raw list of dictionaries against the Pydantic schema."""
    return [StartupProspect.model_validate(item) for item in raw_list]


def generate_tsv_block(raw_list: List[Dict[str, Any]]) -> str:
    """
    Generates Tab-Separated Values (TSV) block for 1-click paste into Google Sheets.
    Columns: [Hook A]\t[Hook B]\t[Hook Source]\t[Best Channels]
    """
    prospects = validate_prospect_payload(raw_list)
    tsv_rows: List[str] = []

    for p in prospects:
        channels_str = ", ".join(p.outreach.best_channels) if p.outreach.best_channels else "Email"
        # Sanitize internal newlines or tabs to preserve TSV column alignment
        clean_hook_a = p.outreach.hook_a.replace("\t", " ").replace("\n", " ").strip()
        clean_hook_b = p.outreach.hook_b.replace("\t", " ").replace("\n", " ").strip()
        clean_source = p.outreach.hook_source.replace("\t", " ").replace("\n", " ").strip()
        row = f"{clean_hook_a}\t{clean_hook_b}\t{clean_source}\t{channels_str}"
        tsv_rows.append(row)

    return "\n".join(tsv_rows)


def export_to_excel(raw_list: List[Dict[str, Any]], output_filepath: str) -> None:
    """
    Creates a styled, professional Excel spreadsheet with auto-fitted columns,
    headers, and data validation chip styling.
    """
    prospects = validate_prospect_payload(raw_list)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Prospects & Outreach"

    # Define Headers
    headers = [
        "Company Name",
        "Website",
        "Category",
        "Description",
        "Launch Date",
        "Founder Name",
        "Role",
        "Founder LinkedIn",
        "Founder X",
        "Work Email",
        "Discord Invite",
        "Community Members",
        "Hook A (Product Trigger)",
        "Hook B (Technical Insight)",
        "Hook Source URL",
        "Best Channels",
    ]
    ws.append(headers)

    # Header Styling
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    center_align = Alignment(horizontal="center", vertical="center", wrap_text=False)
    thin_border = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
    )

    for col_idx, _ in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border

    # Append Data Rows
    for p in prospects:
        channels_str = ", ".join(p.outreach.best_channels) if p.outreach.best_channels else "Email"
        row_data = [
            p.company.name,
            p.company.website,
            p.company.category,
            p.company.one_line_description,
            p.company.launch_date or "N/A",
            p.founder.name,
            p.founder.role,
            p.founder.linkedin_url or "N/A",
            p.founder.x_handle or "N/A",
            p.founder.work_email or "N/A",
            p.community.discord_invite or "N/A",
            p.community.discord_member_count or "N/A",
            p.outreach.hook_a,
            p.outreach.hook_b,
            p.outreach.hook_source,
            channels_str,
        ]
        ws.append(row_data)

    # Style Data Cells & Wrap Long Text for Hooks
    text_align = Alignment(vertical="top", wrap_text=True)
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.font = Font(name="Calibri", size=10)
            cell.alignment = text_align
            cell.border = thin_border

    # Auto-adjust column widths
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val_str = str(cell.value or "")
            # Don't let long hooks blow out the column width calculation
            if len(val_str) > 50:
                val_str = val_str[:50]
            max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    # Fixed wider widths for hook columns
    ws.column_dimensions["M"].width = 45
    ws.column_dimensions["N"].width = 45

    Path(output_filepath).parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_filepath)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export_pipeline.py <input.json> [--excel output.xlsx] [--tsv output.tsv]")
        sys.exit(1)

    json_path = sys.argv[1]
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "--excel" in sys.argv:
        excel_idx = sys.argv.index("--excel") + 1
        export_to_excel(data, sys.argv[excel_idx])
        print(f"Exported Excel to {sys.argv[excel_idx]}")

    if "--tsv" in sys.argv:
        tsv_idx = sys.argv.index("--tsv") + 1
        tsv_content = generate_tsv_block(data)
        with open(sys.argv[tsv_idx], "w", encoding="utf-8") as f:
            f.write(tsv_content)
        print(f"Exported TSV to {sys.argv[tsv_idx]}")
