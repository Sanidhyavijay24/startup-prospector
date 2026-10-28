---
name: startup-prospector
description: >-
  Autonomous startup discovery, active website hygiene audit, founder resolution, and dual-angle outreach hook generation (Hook A & Hook B). Use when the user requests startup sourcing, outbound prospect lists, founder contact enrichment, or export to styled Excel / 1-click Google Sheets TSV.
---

# Autonomous Startup Outreach Prospector Skill

This skill standardizes the end-to-end workflow for discovering early-stage tech and AI startups, verifying live site status, resolving genuine founder profiles, generating peer-to-peer outreach hooks (Hook A and Hook B) with zero fake links or clichés, and exporting the results into styled Excel and Google Sheets TSV.

---

## 1. Interactive Intake Protocol (The Discovery Gate)

When the user triggers this skill, the agent must check if the user's initial prompt contains all necessary parameters. If any key parameter is missing, the agent **must pause and prompt the user** before starting Phase 1 discovery.

### The 4 Intake Questions:
```text
Before I start sourcing, please clarify:

1. Target Niche & Stage: What category and stage are you targeting?
   (e.g., Early-stage AI developer tools, B2B SaaS, pre-seed/seed, YC batches)

2. Your Identity & Product (Optional): Who are you reaching out as?
   - If you are a founder: What is your startup name and a 1-line value proposition?
   - If you are a scout / reviewer / developer: What is your publication, fund, or community?

3. Primary Outreach Angle / Intent:
   [1] Peer Founder / Collaboration: You are a founder connecting with peer builders.
   [2] Technical Integration / Co-Marketing: Proposing an integration between your tool and theirs.
   [3] Review & Media Feature: Featuring them in an upcoming benchmark, guide, or roundup.
   [4] Investor / Scout Inquiry: Sourcing for potential investment, partnership, or advisory.

4. Preferred Discovery Source:
   [1] Hacker News (Show HN / Launch HN - Indie builders & early MVPs)
   [2] GitHub Velocity (Trending OSS with 100+ stars in 60 days & commit emails)
   [3] Y Combinator (Recent batches S24/W24/W25 - Venture-backed SaaS)
   [4] Product Hunt (Top weekly consumer AI & productivity tools)
   [5] Mixed (Recommended - Blends across sources for maximum candidate diversity)

5. Scope & Preferred Channels:
   - How many startups to source? (Default: 10, processed in batches of 5)
   - Preferred outreach channels? (e.g., Discord, LinkedIn, X/Twitter, Cold Email)
```

> **Fast-Forward Rule:** If the user already provided this context in their opening prompt (e.g., *"I am the founder of TraceCLI, find 10 early-stage AI dev tools from YC and GitHub for a co-marketing integration"*), skip the questions and proceed immediately to Phase 1.

### Grounding Hooks to User Identity:
* **When the user is a Founder:** In Hook B, explicitly weave the user's tool into Line 3 (the Bridge):
  > *"We're building [User Startup], a [User Product Description], and saw a natural workflow pairing between [User Value Prop] and what you're doing with [Target Startup]."*
* **When the user is a Reviewer / Scout:** Anchor Line 3 to the upcoming category benchmark or scouting inquiry:
  > *"We are putting together an upcoming [Target Category] benchmark and want to feature [Target Startup]."*

---

## 2. Autonomous Execution Pipeline

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1: MULTI-SOURCE DISCOVERY                 │
│  Execute the designated source engine (or blend in Mixed mode):        │
│  - Hacker News: python .../fetch_hn.py --query "<niche>" --limit N     │
│  - GitHub: python .../fetch_github.py --query "<niche>" --min-stars 100│
│  - Y Combinator: python .../fetch_yc.py --batches S24,W24 --query ...  │
│  - Product Hunt: python .../fetch_ph.py --limit N                      │
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
