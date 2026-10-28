<div align="center">

# startup-prospector

**Autonomous startup discovery, active website hygiene, founder resolution, and grounded dual-angle outreach hook generation for AI coding assistants.**

```
Antigravity Skill  •  Claude Code Compatible  •  Zero API Keys Required  •  Deterministic Quality Gate
```

</div>

---

### The Problem

Outbound prospecting, investor scouting, and developer co-marketing suffer from the same failure modes:
1. **Directory Noise:** Sifting through hundreds of Hacker News, Product Hunt, and YC submissions manually.
2. **Zombie Companies:** 30%+ of early launch sites are dead, parked, or broken SPAs within 90 days.
3. **Identity Collisions:** Mistaking an unrelated corporate registry entity (e.g., a local transport LLC) for the tech founder.
4. **Hallucinated URLs:** LLMs fabricating plausible-looking deep links (e.g., `/blog/launch-v2`) that return 404s.
5. **AI Template Fatigue:** Outreach that sounds like automated spam filled with em dashes, corporate clichés (*"game changer"*, *"testament"*), and generic openers (*"I hope this finds you well"*).

`startup-prospector` packages upstream discovery, programmatic hygiene verification, and grounded copy synthesis into an **Agent-Native Skill**. It leverages the host agent's native browser and search tools alongside deterministic Python scripts to produce verified, ready-to-send pipelines in styled Excel (`.xlsx`) and 1-click Google Sheets TSV.

---

## At a Glance

| Feature | Generic Scraping Scripts | startup-prospector |
| :--- | :--- | :--- |
| **API Costs** | Requires OpenAI, SerpAPI, Hunter.io keys | **$0** (uses host agent intelligence + public endpoints) |
| **Site Verification** | Basic DNS lookup or unchecked | **Full HTTP GET + parked domain regex + SPA audit** |
| **Community Health** | Static link scraping | **Discord public widget audit** (live member/online count) |
| **Founder Match** | Naive string search (high LLC collision) | **Domain-anchored LinkedIn resolution** |
| **Deep Links** | Often hallucinated / 404 dead slugs | **Zero Fake-Slug Rule** (strictly verified 200 OK or blog root) |
| **Tone Quality** | Generic AI spam templates with em dashes | **Deterministic regex linter** (hard-banning AI clichés & em dashes) |
| **Deliverables** | Raw CSV dumps | **Styled navy Excel (.xlsx) + 1-click Google Sheets TSV** |

---

## Architecture

The system operates on an **Agent Brain + Script Muscle** hybrid model:

```text
[ USER PROMPT ] ──► "Find 10 early-stage AI devtools with Discord servers for a media benchmark"
       │
       ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: DISCOVERY (Public APIs & Feeds)                                               │
│ scripts/fetch_hn.py queries Algolia Show HN / Launch HN streams (zero rate-limit pain) │
└──────────────────────────────────────┬─────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: HYGIENE & ACTIVE AUDIT (Deterministic Python)                                 │
│ scripts/audit_hygiene.py filters 404s, parked domains, expired SSLs                   │
│ Extracts real-time community size via Discord widget API without bot credentials       │
└──────────────────────────────────────┬─────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: FOUNDER & CHANGELOG RESOLUTION (Agent Native Tools)                           │
│ Host agent uses search/browser tools with domain-anchoring:                            │
│ "<Company>" "<domain>" (founder OR CEO) site:linkedin.com/in/                          │
│ Resolves most recent milestone from live blog or changelog                             │
└──────────────────────────────────────┬─────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: HOOK SYNTHESIS & QUALITY GATE (LLM Reasoning + Linter)                        │
│ Generates Hook A (Product Trigger) and Hook B (Technical/UX Insight)                   │
│ scripts/lint_hook.py deterministically rejects em dashes, clichés, and length errors   │
└──────────────────────────────────────┬─────────────────────────────────────────────────┘
                                       │
                                       ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: STRUCTURED EXPORT                                                             │
│ scripts/export_pipeline.py formats output/prospects.xlsx and output/prospects.tsv      │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Copy Comparison: Why Conversion Rates Matter

### Standard AI Outreach (Low Conversion)
> *"I hope this email finds you well! Your cutting-edge AI diff engine is a true game changer—a testament to your team's revolutionary work in navigating the devtools landscape. Let's delve into how we can collaborate."*

* **Why it fails:** Generic opener, em dash (`—`), corporate buzzwords (*"cutting-edge"*, *"game changer"*, *"testament"*, *"delve"*), zero specific product observation.

### startup-prospector Output (Peer-to-Peer, High Conversion)

#### Hook A (Product / Milestone Trigger — Ideal for LinkedIn & X DMs)
> *"Read your post from earlier this month introducing the new terminal diff engine. Giving engineers git-native review controls without forcing another heavy IDE extension solves the exact friction developers complain about. We are putting together an AI developer tooling benchmark and want to feature DevFlow AI."*

#### Hook B (Workflow / Architecture Insight — Ideal for Cold Email)
> *"DevFlow AI has stood out for keeping the CLI interaction instantaneous while other platforms overload their sidebars with complicated settings. For everyday refactoring, a lightweight terminal workflow beats enterprise GUI tools every time. Would love to feature DevFlow AI in our upcoming developer tools guide."*

---

## Installation & Setup

### Method 1: Agent-Assisted Installation (Zero Manual Commands)

If you are already inside an agent runtime (Antigravity IDE, Claude Code, Cursor), paste this prompt:

```text
Install the startup-prospector skill from https://github.com/Sanidhyavijay24/startup-prospector.git into my workspace.
```

Your assistant will autonomously clone the skill into `.agents/skills/startup-prospector` and configure dependencies.

---

### Method 2: 1-Line Terminal Installation

#### Antigravity IDE & Antigravity CLI (`agy`)

**For the current project workspace:**
```bash
# macOS / Linux
git clone https://github.com/Sanidhyavijay24/startup-prospector.git .agents/skills/startup-prospector && pip install -r .agents/skills/startup-prospector/requirements.txt

# Windows (PowerShell)
git clone https://github.com/Sanidhyavijay24/startup-prospector.git .agents/skills/startup-prospector; pip install -r .agents/skills/startup-prospector/requirements.txt
```

**Global installation (available in every project on your machine):**
```bash
# macOS / Linux
git clone https://github.com/Sanidhyavijay24/startup-prospector.git ~/.gemini/config/skills/startup-prospector && pip install -r ~/.gemini/config/skills/startup-prospector/requirements.txt

# Windows (PowerShell)
git clone https://github.com/Sanidhyavijay24/startup-prospector.git "$HOME\.gemini\config\skills\startup-prospector"; pip install -r "$HOME\.gemini\config\skills\startup-prospector\requirements.txt"
```

#### Claude Code CLI (`claude`)

Run in your active project directory:
```bash
git clone https://github.com/Sanidhyavijay24/startup-prospector.git .agents/skills/startup-prospector && pip install -r .agents/skills/startup-prospector/requirements.txt
echo "When asked to prospect startups or find founders, follow .agents/skills/startup-prospector/SKILL.md" >> CLAUDE.md
```

---

## End-to-End Walkthrough

### 1. Triggering via Prompt & Adaptive Intake

You can trigger the skill with a single prompt. If your instruction is high-level, the agent automatically initiates an **Intake Interview** before spending compute:

```text
User: @startup-prospector Find some AI developer tools for outreach.

Agent: Before I start sourcing, please clarify:
1. Target Niche & Stage: (e.g., Early-stage AI developer tools, pre-seed/seed)
2. Your Identity (Optional): Who are you reaching out as? (e.g., "Founder of TraceCLI")
3. Primary Intent: [1] Peer Founder, [2] Integration, [3] Review Benchmark, [4] Investor Scout
4. Batch Size: (Default: 10, processed in batches of 5)
```

**Fast-Forward Mode:** If you provide your context upfront, the agent skips the intake interview and proceeds directly:
```text
@startup-prospector I am the founder of TraceCLI (terminal logger). Find 10 early-stage AI devtools with Discord communities for a founder-to-founder co-marketing integration.
```

The skill executes in **atomic batches of 5** to preserve context window reasoning and prevent hallucination drift.

---

### 2. Standalone Script Execution

Every module can also be invoked as a standalone CLI tool without an LLM:

#### A. Discover Candidates via 4 Zero-Cost Ingestion Engines

**1. Hacker News Algolia Stream (Indie hackers & early MVPs):**
```bash
python .agents/skills/startup-prospector/scripts/fetch_hn.py --query "developer" --limit 5
```

**2. GitHub Star Velocity (100+ stars in 60 days + git commit author email extractor):**
```bash
python .agents/skills/startup-prospector/scripts/fetch_github.py --query "agent" --days 60 --min-stars 100 --limit 5
```
```json
[
  {
    "name": "magpie",
    "one_line_description": "Every agent's model in one place",
    "website": "https://usemagpie.ai",
    "stars": 24560,
    "founder_handle": "@yetone",
    "founder_name": "yetone",
    "founder_email": "yetoneful@gmail.com",
    "github_repo": "https://github.com/yetone/magpie"
  }
]
```

**3. Y Combinator Public Directory (Recent batches S24/W24/W25 - Active startups only):**
```bash
python .agents/skills/startup-prospector/scripts/fetch_yc.py --batches S24,W24 --query "ai" --limit 5
```
```json
[
  {
    "name": "Merlin AI",
    "one_line_description": "AI powered ERP for Construction",
    "website": "https://www.merlinai.co",
    "batch": "Summer 2024",
    "status": "Active",
    "team_size": 19,
    "yc_profile_url": "https://www.ycombinator.com/companies/merlin-ai"
  }
]
```

**4. Product Hunt Weekly Launches (Public Atom feed reader):**
```bash
python .agents/skills/startup-prospector/scripts/fetch_ph.py --limit 5
```

#### B. Audit Website Liveness & Community Health
```bash
python .agents/skills/startup-prospector/scripts/audit_hygiene.py https://devflow.example.com
```
```json
{
  "url": "https://devflow.example.com",
  "is_live": true,
  "status_code": 200,
  "final_url": "https://devflow.example.com/",
  "is_parked": false,
  "error": null
}
```

#### C. Run the Deterministic Tone & Syntax Linter
```bash
python .agents/skills/startup-prospector/scripts/lint_hook.py "Your new tool is a game changer—it elevates developer workflow. Check our benchmark."
```
```json
{
  "is_valid": false,
  "violations": [
    "Em dash detected ('—' or '--'). Use standard commas or periods.",
    "Banned buzzword or cliché detected: 'game changer'.",
    "Hook too short: 13 words. Must be between 25 and 85 words."
  ],
  "sentence_count": 2,
  "word_count": 13
}
```

#### D. Export Enriched Pipeline to Excel & Google Sheets TSV
```bash
python .agents/skills/startup-prospector/scripts/export_pipeline.py output/payload.json --excel output/prospects.xlsx --tsv output/prospects.tsv
```

---

## Output Deliverables

### 1. Styled Excel Spreadsheet (`output/prospects.xlsx`)
Built with `openpyxl`, featuring navy table headers (`#1E293B`), wrapped multi-line cells for outreach copy, auto-adjusted column dimensions, and community sizing:

| Company Name | Website | Founder Name | Role | Founder LinkedIn | Discord Invite | Members | Hook A (Product Trigger) | Hook B (Technical Insight) | Hook Source | Best Channels |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DevFlow AI** | `https://devflow.example.com` | Alex Mercer | Founder & CEO | `linkedin.com/in/alexmercer-dev` | `discord.gg/devflow` | 1,420 | *Read your post from earlier this month introducing the new terminal diff engine...* | *DevFlow AI has stood out for keeping the CLI interaction instantaneous...* | `https://devflow.example.com/blog` | Discord, LinkedIn, X |

### 2. 1-Click Google Sheets TSV (`output/prospects.tsv`)
Tab-separated values engineered for instant pasting. Click cell **AD** in your master Google Sheet, press `Ctrl + V`, and seamlessly populate:
* **Col AD:** Hook A
* **Col AE:** Hook B
* **Col AF:** Hook Source URL
* **Col AG:** Best Channels

---

## Pluggable Campaign Intents

Customize the bridge in `templates/campaign_intents.json`:

* **`review_media` (Default):** *"We are putting together an upcoming [Category] benchmark and would love to feature [Company Name]."*
* **`investor_scout`:** *"We actively scout high-momentum early-stage founders in [Category] and would love to learn more about your roadmap."*
* **`partnership_integration`:** *"We are building developer workflows in the [Category] space and see a natural integration with what [Company Name] is doing."*
* **`founder_feedback`:** *"Currently testing early tooling in the [Category] space and wanted to share a couple UX observations with you directly."*

---

## Quality Assurance & Verification

The test suite covers schema validation, HTTP response mocking, edge cases in Show HN post parsing, and regex quality bounds:

```bash
python -m pytest tests/ -v
```

```text
tests/test_exporter.py::test_validate_prospect_payload PASSED            [  7%]
tests/test_exporter.py::test_generate_tsv_block PASSED                   [ 15%]
tests/test_exporter.py::test_export_to_excel PASSED                      [ 23%]
tests/test_fetch_hn.py::test_clean_project_name_variants PASSED          [ 30%]
tests/test_fetch_hn.py::test_fetch_show_hn_tools_mock PASSED             [ 38%]
tests/test_hygiene.py::test_url_liveness_success PASSED                  [ 46%]
tests/test_hygiene.py::test_url_liveness_404_failure PASSED              [ 53%]
tests/test_hygiene.py::test_parked_domain_detection PASSED               [ 61%]
tests/test_hygiene.py::test_extract_discord_stats_success PASSED         [ 69%]
tests/test_linter.py::test_clean_hook_passes PASSED                      [ 76%]
tests/test_linter.py::test_em_dash_fails PASSED                          [ 84%]
tests/test_linter.py::test_corporate_buzzwords_fail PASSED               [ 92%]
tests/test_linter.py::test_sentence_count_bounds PASSED                  [100%]

============================= 13 passed in 0.38s ==============================
```

---

## Project Structure

```text
startup-prospector/
├── README.md                                       # Documentation & usage guide
├── LICENSE                                         # MIT License
├── context.md                                      # Project single source of truth & ledger
├── requirements.txt                                # Python dependencies
├── output/                                         # Generated .xlsx and .tsv exports
├── tests/
│   ├── conftest.py                                 # Test fixtures & module path setup
│   ├── test_linter.py                              # Quality gate tone tests
│   ├── test_hygiene.py                             # URL audit & Discord widget tests
│   ├── test_fetch_hn.py                            # Show HN parser & API client tests
│   └── test_exporter.py                            # TSV & Excel export tests
└── .agents/
    └── skills/
        └── startup-prospector/
            ├── SKILL.md                            # Antigravity skill specification
            ├── scripts/
            │   ├── fetch_hn.py                     # Algolia HN discovery engine
            │   ├── audit_hygiene.py                # Liveness & Discord community checker
            │   ├── lint_hook.py                    # Deterministic regex quality gate
            │   └── export_pipeline.py              # Styled Excel & TSV exporter
            ├── templates/
            │   ├── campaign_intents.json           # Pluggable value prop bridges
            │   └── hook_guidelines.md              # 3-line formula & copy rubrics
            └── references/
                ├── anti_hallucination.md           # Zero fake-slug & date anchoring rules
                └── directory_endpoints.md          # Public discovery endpoints documentation
```

---

## License & Author

* **Author:** Sanidhya Vijay
* **License:** [MIT License](LICENSE)
