# Job Search

Search all configured sources for jobs matching the user profile.

## Prerequisites
- `data/user_profile.md` must exist. If not, tell the user to run the profile builder first.
- Read `data/sources.md` for crawl learnings and source-specific notes.
- Read `data/seen_jobs.json` to know what's already been surfaced.

## Search Strategy (updated 2026-04-06)

This profile targets VP/CTO/Head-level engineering leadership at large (200+ employee) companies. Most public job APIs skew junior/mid-level. The search strategy therefore prioritizes:

1. **Direct career pages** of target companies (via WebSearch)
2. **WebSearch** across Glassdoor, LinkedIn snippets, and executive job boards
3. **JSearch** (Google for Jobs aggregator) — best structured API for this level
4. **Adzuna** — useful for UK roles, filter out banking "VP" titles
5. **MyCareersFuture** — useful for Singapore CTO/VP roles
6. **Indeed MCP** — deprioritized, weak for executive roles

**Skip these** (no executive-level results): RemoteOK, Arbeitnow, Himalayas

## Procedure

1. **Read the profile and learned preferences**: Load `data/user_profile.md` including the Learned Preferences section. Extract:
   - Target titles and adjacent titles
   - Target and avoid companies
   - Target locations with country codes
   - Comp thresholds (UK: £160K+, Singapore: SGD 25K+/month, US: $350K+, Tokyo: competitive)
   - Dealbreakers (Musk companies, Palantir, crypto, consulting, defense)
   - Learned filters (no sales-facing roles, no small companies, verify freshness)

2. **Search target company career pages** (highest priority):
   Use WebSearch for each target company:
   - `site:careers.google.com "VP engineering" OR "director engineering" OR "head of AI"`
   - `site:boards.greenhouse.io/anthropic "engineering"` (or similar ATS)
   - `site:openai.com/careers "engineering"`
   - `site:careers.microsoft.com "VP engineering"`
   - etc. for: Waymo, Apple, Disney, Sony, LinkedIn
   
   Also search for similar-caliber companies not on the explicit list:
   - `"VP of Engineering" OR "Head of AI" site:lever.co OR site:greenhouse.io 2026`

3. **Search executive job boards and aggregators** (WebSearch):
   - `"VP of Engineering" OR CTO remote AI ML 2026 hiring -recruiter`
   - `"VP Engineering" OR "Head of Engineering" London 2026`
   - `"VP Engineering" OR CTO Tokyo Japan 2026 english`
   - `"VP Engineering" OR CTO Singapore 2026`
   - `"Head of AI" OR "Chief AI Officer" hiring 2026`
   - Glassdoor, LinkedIn job snippets, Wellfound for each target location

4. **Search structured APIs** (JSearch, Adzuna, MCF):
   
   a. **JSearch** — Run for key title+location combos:
      ```bash
      python3 scripts/search.py --source jsearch --query "<title>" --location "<location>" --country <cc> --limit 20
      ```
   
   b. **Adzuna** — UK and Singapore only:
      ```bash
      python3 scripts/search.py --source adzuna --query "<title>" --location "<location>" --country <cc> --limit 15
      ```
      Post-filter: remove results where "VP" is a banking level title (Citi, JPMorgan, Goldman, Barclays, HSBC, Deutsche Bank, etc.)
   
   c. **MyCareersFuture** — Singapore only:
      ```bash
      python3 scripts/search.py --source mycareersfuture --query "CTO" --limit 15
      python3 scripts/search.py --source mycareersfuture --query "VP engineering" --limit 15
      ```

   d. **Indeed MCP** — Run 1-2 broad searches only, don't rely on it:
      - `mcp__claude_ai_Indeed__search_jobs` with "VP Engineering CTO" in key locations

5. **Verify job freshness**: For the most promising results, use WebFetch to confirm:
   - The job posting page loads
   - The posting date is within the last 30 days
   - The role is still open
   Drop any that fail verification.

6. **Pre-filter before ranking**: Remove jobs that fail ANY of these:
   - Company likely < 200 employees (unless target company)
   - Comp listed and below thresholds
   - Title contains "Field", "Solutions", "Pre-sales"
   - Company is in avoid list or avoid industries
   - Posting is older than 30 days
   - Link is dead

7. **Save raw results**: Write to `data/runs/YYYY-MM-DD_raw.json`.

8. **Report**: Tell the user how many jobs were found from each source.

## Notes
- If a source fails (API error, rate limit), log the error and continue.
- Record any issues in the "Crawl Learnings" section of `data/sources.md`.
- Quality over quantity — 3 well-vetted roles beat 10 unverified ones.
