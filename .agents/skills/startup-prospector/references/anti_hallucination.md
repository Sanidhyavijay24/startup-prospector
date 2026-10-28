# Anti-Hallucination & Grounding Reference

This reference establishes mandatory ground rules to prevent URL hallucinations, outdated claims, and identity mismatches during autonomous prospecting.

---

## 1. The Zero Fake-Slug Rule

* **The Problem:** LLM agents frequently extrapolate or invent plausible-looking subpaths (such as `company.com/blog/v2-launch-announcement` or `company.com/press/series-a`). These paths almost always return HTTP 404 Not Found errors.
* **The Rule:**
  1. Only cite deep links that have been requested and returned `HTTP 200 OK`.
  2. If the deep link cannot be verified (e.g. Cloudflare anti-bot blocks), **always fallback to the verified announcement hub or changelog root** (e.g. `https://company.com/blog` or `https://company.com/changelog`) where the update sits at the top.
  3. Never guess or hallucinate a sub-URL.

---

## 2. Real-Time Date Anchoring

* **The Problem:** Agents citing two-year-old updates (e.g. "Saw your 2024 launch") when looking at a live startup in late 2025 or 2026. This destroys outreach credibility.
* **The Rule:**
  1. Always query the most recent public milestones first (within the last 30 to 90 days).
  2. If the newest milestone is from several months ago, phrase it by topic rather than asserting it happened yesterday.
  3. Never claim an old MVP launch is "recent" if a newer major feature update or v2 release exists.

---

## 3. False Registry Match Prevention (LLC Collision)

* **The Problem:** In corporate registries and LinkedIn searches, early-stage SaaS startups frequently share identical names with unrelated brick-and-mortar entities (e.g., "Aura AI" vs "Aura Logistics LLC").
* **The Rule:**
  1. **Domain-Anchored Matching:** Always search for the founder by pairing company name + domain root + keywords:
     `"<Company Name>" "<canonical_domain>" (founder OR "co-founder" OR CEO) site:linkedin.com/in/`
  2. **Experience Verification:** Confirm that the founder's active LinkedIn experience card points to the specific software product and domain, not an unrelated business.
  3. If a founder cannot be verified with confidence, leave the email and handle blank rather than assigning an unrelated person.
