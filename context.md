# Project Ledger: Startup Outreach Prospector Skill

## 1. Project Overview
Autonomous agent-native skill designed for Antigravity, Gemini, and AI coding assistants. Converts high-level startup criteria into a verified, enriched pipeline with human-sounding dual-hook outreach openers (Hook A & Hook B) with zero fake links or hallucinations, exported to styled Excel (`.xlsx`) and 1-click Google Sheets TSV.

## 2. Tech Stack & Environment
- **Runtime:** Python 3.10+ (Active Conda Environment)
- **Dependencies:** `requests`, `beautifulsoup4`, `openpyxl`, `pydantic`, `pytest`
- **Agent Integration:** Antigravity Customization System (`.agents/skills/startup-prospector/SKILL.md`)
- **Testing Framework:** `pytest`

## 3. Architecture & Data Flow
```
[User / Agent Input] (Niche, Batch Size, Intent Profile)
        │
        ▼
[Phase 1: Discovery] ──► fetch_hn.py / YC / PH public feeds
        │
        ▼
[Phase 2: Hygiene Filter] ──► audit_hygiene.py (HTTP 200, redirect check, Discord widget)
        │
        ▼
[Phase 3: Founder & Milestone Resolution] ──► Host Agent Browser / Web Search
        │
        ▼
[Phase 4: Hook Synthesis & Linting] ──► LLM generation + lint_hook.py (Deterministic quality gate)
        │
        ▼
[Phase 5: Structured Export] ──► export_pipeline.py (.xlsx with styled tables + TSV 1-click paste)
```

## 4. Feature Status Checklist
- [x] `context.md` ledger established
- [x] `requirements.txt` configured
- [x] Quality gate: `lint_hook.py` (No em-dashes, no buzzwords, sentence count) - 100% verified
- [x] Hygiene auditor: `audit_hygiene.py` (HTTP status, SSL, parked domain, Discord stats) - 100% verified
- [x] Discovery engine: `fetch_hn.py` (Algolia HN API integration with clean name parser) - 100% verified
- [x] Exporter engine: `export_pipeline.py` (Styled Excel + 1-click TSV) - 100% verified
- [x] Templates & references (`campaign_intents.json`, `anti_hallucination.md`, etc.) - 100% verified
- [x] Core Skill definition: `SKILL.md` with complete agent rubrics - 100% verified
- [x] Test suite: 13/13 `pytest` unit tests passing
- [x] Live verification with real sample batch (Show HN, live HTTP 200, styled .xlsx, and TSV)
- [x] Repository cleanup: converted blueprint to production `README.md`, added `LICENSE`, cleaned obsolete prototype folders
- [x] Multi-agent install guides documented in `README.md` (Agent-prompt, 1-line Antigravity workspace/global, and Claude Code CLI)
- [x] Canonical GitHub repository URL linked: `https://github.com/Sanidhyavijay24/startup-prospector.git`
- [x] High-end README redesign completed: removed tacky emojis/badges, added competitive breakdown table, side-by-side copy comparison, and full terminal trace walkthroughs
- [x] Interactive Intake Protocol implemented: 4-question intake gate with founder persona adaptation, dynamic co-marketing bridge templates, and fast-forward mode

## 5. Data Models
### StartupRecord Schema (Pydantic / JSON)
```python
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
    best_channels: list[str]

class StartupProspect(BaseModel):
    company: Company
    founder: Founder
    community: Community
    outreach: Outreach
```

## 6. API Contracts
- `fetch_hn.py`: CLI returning JSON array of candidate tools from Algolia HN search API.
- `audit_hygiene.py`: Takes URL list or single URL, returns status, final redirect URL, and liveness flag.
- `lint_hook.py`: Takes hook text string or JSON, returns `{ "pass": bool, "violations": list[str] }`.
- `export_pipeline.py`: Takes validated JSON array of `StartupProspect`, outputs `.xlsx` and `.tsv`.

## 7. Technical Debt & Notes
- None currently.
