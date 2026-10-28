---
name: startup-prospector
description: >-
  Autonomous startup discovery, active website hygiene audit, founder resolution, and dual-angle outreach hook generation (Hook A & Hook B). Use when the user requests startup sourcing, outbound prospect lists, founder contact enrichment, or export to styled Excel / 1-click Google Sheets TSV.
---

# Autonomous Startup Outreach Prospector Skill

This skill standardizes the end-to-end workflow for discovering early-stage tech and AI startups, verifying live site status, resolving genuine founder profiles, generating peer-to-peer outreach hooks (Hook A and Hook B) with zero fake links or clichés, and exporting the results into styled Excel and Google Sheets TSV.

---

## 1. Input Parsing & Intent Configuration

When the user triggers this skill:
1. **Identify the Search Criteria:**
   * Target Niche / Category (e.g. *"AI Developer Tools"*, *"B2B SaaS"*, *"Local LLM agents"*).
   * Target Batch Size (default is **10** startups; execute in sub-batches of 5).
   * Target Intent Profile (refer to `templates/campaign_intents.json`):
     - `review_media`: Review / Media Benchmark feature (default).
     - `investor_scout`: Venture scout / investor inquiry.
     - `partnership_integration`: Co-marketing or API integration.
     - `founder_feedback`: Peer-to-peer product testing feedback.

---

## 2. Autonomous Execution Pipeline

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: MULTI-SOURCE DISCOVERY                 │
│  - Run: python .agents/skills/startup-prospector/scripts/fetch_hn.py   │
│    --query "<niche>" --limit <batch_size * 2>                          │
│  - Or search Y Combinator / Product Hunt via web search                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        PHASE 2: HYGIENE & AUDIT                        │
│  - Run: python .agents/skills/startup-prospector/scripts/audit_hygiene.py │
│  - Filter out: 404s, parked domains, expired SSL, or dead landing pages│
│  - If Discord invite found: query Discord widget API for member count  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: FOUNDER & CHANGELOG RESEARCH               │
│  - Query founder identity using domain-anchored LinkedIn searches:     │
│    "<Company>" "<domain>" (founder OR CEO) site:linkedin.com/in/       │
│  - Inspect official changelog, blog, or recent GitHub releases         │
│  - Verify recent milestones (from late 2025 or 2026)                   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   PHASE 4: HOOK SYNTHESIS & QUALITY GATE               │
│  - Synthesize Hook A (Product trigger) & Hook B (Technical insight)    │
│  - Follow templates/hook_guidelines.md (strictly 2-3 sentences)        │
│  - Execute: python .../lint_hook.py "<hook text>"                      │
│    Reject any hook containing em dashes (—) or corporate buzzwords     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         PHASE 5: STRUCTURED EXPORT                     │
│  - Save candidate records to a temporary JSON file                     │
│  - Run: python .../export_pipeline.py payload.json                     │
│    --excel output/prospects.xlsx --tsv output/prospects.tsv            │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Strict Anti-Hallucination & Quality Protocol

Before adding any startup to the output:

1. **Zero Fake-Slug Rule:**
   * **NEVER synthesize or guess sub-URLs** (e.g. `/blog/launch-v2/` or `/press/seed-round/`).
   * Verify deep links return `HTTP 200 OK` or fallback safely to the verified announcement hub (`https://company.com/blog/` or `https://company.com/changelog`).
2. **Real-Time Date Anchoring:**
   * Always prioritize current updates (within the last 30-90 days).
   * Never frame a two-year-old launch as "recent" if newer changelog updates exist.
3. **Founder Identity Validation:**
   * Ensure the person is the founder/CEO of the specific software company, avoiding unrelated delivery or transport LLCs with identical names.
4. **Tone & Syntax Linter:**
   * Run every hook through `scripts/lint_hook.py`.
   * Hard ban on em dashes (`—` or `--`).
   * Hard ban on AI clichés (`delve`, `game changer`, `testament`, `cutting-edge`, `revolutionary`, `unleash`, `elevate`).

---

## 4. Batching Guideline (Prevent Context Bloat)

To maintain high reasoning quality and prevent context window exhaustion:
* Process prospects in **batches of 5**.
* For each batch of 5: discover $\to$ audit $\to$ research changelog $\to$ draft hooks $\to$ run linter $\to$ append to `output/raw_prospects.json`.
* Once the desired count is reached, run `scripts/export_pipeline.py` once to build the final styled Excel and TSV files.

---

## 5. Output Deliverables

The skill produces two primary files in the workspace `output/` directory:
1. `output/prospects_YYYY-MM-DD.xlsx`: Formatted Excel workbook with navy headers, auto-adjusted column widths, wrapped text for hooks, and multi-channel chips.
2. `output/prospects_latest.tsv`: Tab-separated values formatted for direct 1-click paste into Google Sheets columns (Hook A, Hook B, Hook Source, Best Channels).
