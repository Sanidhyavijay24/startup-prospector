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

## 2. Discord Public Widget API

* **Usage:** Instant discovery of community size and active member presence without joining the server.
* **Endpoint:**
  `GET https://discord.com/api/v8/invites/{invite_code}?with_counts=true`
* **Example:**
  `https://discord.com/api/v8/invites/reactiflux?with_counts=true`
* **Response Data:**
  * `approximate_member_count`: Total registered members.
  * `approximate_presence_count`: Real-time online members.
  * `guild.name`: Official server name.

---

## 3. GitHub Developer Contact Extraction

* **Usage:** For open-source and developer-focused tools, founders commit directly to the repository.
* **Technique:**
  * Add `.patch` to any recent commit URL on GitHub (e.g. `https://github.com/org/repo/commit/{hash}.patch`).
  * The git patch header contains the author's verified name and git commit email:
    `From: Jane Doe <jane@example.com>`
  * Provides verified technical founder contact info without third-party email data brokers.
