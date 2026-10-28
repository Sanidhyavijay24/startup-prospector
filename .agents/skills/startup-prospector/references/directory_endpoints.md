# Public Directory & Discovery APIs Reference

This reference documents free, public, and rate-limit friendly endpoints that the agent and helper scripts can query for autonomous startup sourcing without paid API keys.

---

## 1. Hacker News Algolia Search API

* **Base URL:** `https://hn.algolia.com/api/v1`
* **Rate Limits:** Extremely generous (up to 10,000 requests/hour from public IPs).
* **Endpoints:**
  * **Show HN Chronological:**
    `GET https://hn.algolia.com/api/v1/search_by_date?tags=show_hn&hitsPerPage=30`
  * **Keyword Search on Show HN:**
    `GET https://hn.algolia.com/api/v1/search?query=ai&tags=show_hn&hitsPerPage=30`
* **Response Keys:**
  * `title`: Project title with tagline.
  * `url`: Canonical startup website.
  * `author`: Hacker News username of the submitter/founder.
  * `objectID`: Thread ID (HN discussion URL: `https://news.ycombinator.com/item?id={objectID}`).
  * `points`: Number of community upvotes.
  * `created_at`: Submission timestamp.

---

## 2. GitHub Search & Commit Author Extractor

* **Search API:** `GET https://api.github.com/search/repositories?q={query}+created:>{date}+stars:>={min_stars}&sort=stars&order=desc`
* **Rate Limits:** 10 unauthenticated requests/min, or 5,000/hr with `GITHUB_TOKEN`.
* **Founder Email Extraction via Commits API / Patch:**
  * `GET https://api.github.com/repos/{owner}/{repo}/commits?per_page=5`
  * Or append `.patch` to commit URL: `https://github.com/{owner}/{repo}/commit/{sha}.patch`
  * Header regex: `^From:\s*([^<\n]+)<([^>\n]+)>`
  * Bot filtering: Exclude `[bot]`, `users.noreply.github.com`, `actions@github.com`.

---

## 3. Y Combinator Public Algolia Index

* **Endpoint:** `POST https://45bwzj1sgc-dsn.algolia.net/1/indexes/YCCompany_production/query`
* **Authentication:** Public search-only credentials embedded in `ycombinator.com/companies` frontend:
  * Application ID: `45BWZJ1SGC`
  * Headers: `Referer: https://www.ycombinator.com/`
* **Facet Filters:**
  * Batches: `["batch:Summer 2024", "batch:Winter 2024", "batch:Summer 2025"]`
* **Response Keys:**
  * `name`: Startup name.
  * `website`: Canonical website URL.
  * `one_liner`: Elevator pitch.
  * `status`: Active vs Inactive / Acquired.
  * `team_size`: Current headcount.
  * `subindustry`: Category taxonomy.
  * `slug`: YC profile URL (`https://www.ycombinator.com/companies/{slug}`).

---

## 4. Product Hunt Public Atom Feed

* **Endpoint:** `GET https://www.producthunt.com/feed`
* **Format:** Atom `<feed>` XML containing 50 latest product launches.
* **Extraction:**
  * `<title>`: Product name and tagline.
  * `<link href="...">`: Product Hunt post URL and product page.
  * `<content>`: Cleaned HTML description and value proposition.
  * `<published>`: Launch timestamp.

---

## 5. Discord Public Widget API

* **Usage:** Instant discovery of community size and active member presence without joining the server.
* **Endpoint:**
  `GET https://discord.com/api/v8/invites/{invite_code}?with_counts=true`
* **Example:**
  `https://discord.com/api/v8/invites/reactiflux?with_counts=true`
* **Response Data:**
  * `approximate_member_count`: Total registered members.
  * `approximate_presence_count`: Real-time online members.
  * `guild.name`: Official server name.
