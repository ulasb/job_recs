# Job Presenter

Deduplicate, rank, and present the best jobs from today's search.

## Prerequisites
- Today's raw results must exist at `data/runs/YYYY-MM-DD_raw.json`. If not, tell the user to run `/project:search` first.
- `data/user_profile.md` must exist.

## Procedure

1. **Load data**:
   - Read `data/runs/YYYY-MM-DD_raw.json` (today's raw results)
   - Read `data/seen_jobs.json` (previously seen jobs)
   - Read `data/user_profile.md` (user preferences)

2. **Deduplicate**:
   - Build a set of all `dedup_key` values from `data/seen_jobs.json`
   - Remove any job from raw results whose `dedup_key` is already in the set
   - Also deduplicate within today's results (same job found on multiple sources — keep the one with the most complete data)
   - Report how many duplicates were removed

3. **Rank the remaining jobs** by relevance to the user profile. Consider:
   - **Title match**: How closely does the job title match target titles? (highest weight)
   - **Location match**: Is it in a preferred location or remote? (high weight)
   - **Skills alignment**: Does the summary mention skills the user has? (medium weight)
   - **Company fit**: Does the company size/industry match preferences? (medium weight)
   - **Compensation**: Is salary in range (if available)? (medium weight)
   - **Dealbreakers**: Any dealbreakers triggered? (instant disqualify)
   - **Learned preferences**: Use feedback patterns from the profile's "Learned Preferences" section

   Assign a `relevance_score` from 1-10 to each job.

4. **Select top 10** jobs by relevance score.

5. **Present to the user** in a clear markdown format:
   ```
   ## Top Jobs for YYYY-MM-DD

   ### 1. [Job Title](apply_url) — Company Name
   📍 Location | 💰 Salary | 🏢 Source
   **Why this matches**: Brief explanation of relevance
   **Score**: X/10

   ---
   ```

6. **Save the daily report** to `data/runs/YYYY-MM-DD.md`.

7. **Update seen_jobs.json**: Append ALL new jobs from today (not just top 10) to `data/seen_jobs.json` with `feedback: null`. This prevents them from appearing in future runs.

## Hard Filters (updated 2026-04-06)

Before ranking, remove any job that fails these checks:
- **Comp below threshold**: UK < £160K base, Singapore < SGD 25K/month, US < $350K base, Tokyo must be explicitly competitive
- **Company too small**: Likely < 200 employees (unless on target companies list)
- **Wrong role type**: "Field CTO", pre-sales, solutions architect, customer-facing technical roles
- **Stale posting**: Older than 30 days or link doesn't load
- **Dealbreaker company/industry**: Musk-affiliated, Palantir, crypto/Web3, consulting/staffing, defense
- **Banking VP titles**: Citi, JPMorgan, Goldman, etc. where "VP" is a seniority band, not a functional title

## Notes
- Quality over quantity: presenting 3 strong, verified roles is better than 10 unvetted ones.
- If there are zero new jobs after filtering, tell the user honestly and suggest which target company career pages to check directly.
- Always include the apply URL so the user can click through directly.
- For each job, note the company size/headcount if discoverable.
