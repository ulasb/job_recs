# Job Recommendation System

A daily pipeline that finds, ranks, and presents job opportunities based on a user profile. Run via custom commands (`/project:profile`, `/project:search`, `/project:present`, `/project:feedback`, `/project:run`).

## Architecture

The system has 5 pipeline steps, each with a custom command:

1. **Profile Builder** (`/project:profile`) — Build/update `data/user_profile.md` from the user's resume and interactive Q&A. Uses Indeed `get_resume` MCP tool as starting point. Only runs interactively.

2. **Job Search** (`/project:search`) — Query all configured sources for jobs matching the profile. Outputs `data/runs/YYYY-MM-DD_raw.json`. Sources:
   - Indeed MCP (direct tool call)
   - JSearch, Adzuna, RemoteOK, Arbeitnow, Himalayas, MyCareersFuture (via `scripts/search.py`)
   - WebSearch (direct tool call, for Asian job boards and gap-filling)

3. **Presenter** (`/project:present`) — Deduplicate against `data/seen_jobs.json`, rank by relevance to profile, present top 10. Outputs `data/runs/YYYY-MM-DD.md` and appends to `data/seen_jobs.json`.

4. **Feedback** (`/project:feedback`) — Collect yes/no + optional reasons on presented jobs. Updates `data/seen_jobs.json` with feedback and tunes `data/user_profile.md` preferences.

5. **Full Pipeline** (`/project:run`) — Runs steps 2-3 in sequence (skips profile if it exists). Step 4 (feedback) is always interactive.

## Data Files

### `data/user_profile.md`
User profile built from resume + Q&A. Contains:
- Professional summary, skills, experience level
- Job preferences: titles, industries, company size
- Location preferences: countries, cities, remote willingness, relocation flexibility
- Compensation expectations
- Dealbreakers and strong preferences
- Learned preferences (updated from feedback over time)

### `data/sources.md`
Configuration for all job sources: endpoints, coverage areas, search queries to run, and learnings from prior crawls.

### `data/seen_jobs.json`
Array of all jobs ever surfaced. Each entry:
```json
{
  "id": "indeed_abc123",
  "source": "indeed",
  "title": "Software Engineer",
  "company": "Acme Corp",
  "location": "Tokyo, Japan",
  "url": "https://...",
  "date_found": "2026-04-06",
  "date_posted": "2026-04-04",
  "salary": "$120k-$150k",
  "summary": "Brief description...",
  "relevance_score": 8.5,
  "feedback": null,
  "feedback_reason": null,
  "dedup_key": "acme_corp|software_engineer|tokyo_japan"
}
```

### `data/runs/YYYY-MM-DD_raw.json`
Raw search results from all sources for a given day, before dedup/ranking.

### `data/runs/YYYY-MM-DD.md`
Daily report with top ranked jobs, presented to the user.

## Deduplication

Jobs are deduped using a composite key: `normalize(company) | normalize(title) | normalize(location)`. Normalization: lowercase, strip punctuation, collapse whitespace. A job is a duplicate if its dedup_key exists in `data/seen_jobs.json`.

## Search Script Usage

```bash
# Search a specific source
python3 scripts/search.py --source remoteok --query "engineer"
python3 scripts/search.py --source jsearch --query "software engineer" --location "Tokyo" --country JP
python3 scripts/search.py --source adzuna --query "developer" --location "London" --country gb
python3 scripts/search.py --source arbeitnow --query "backend"
python3 scripts/search.py --source himalayas --query "engineering"
python3 scripts/search.py --source mycareersfuture --query "software engineer"

# Search all sources at once
python3 scripts/search.py --source all --query "software engineer" --location "remote"
```

Output is always a JSON array of job objects with normalized fields.

## API Keys

Stored in `.env` (gitignored). See `.env.example` for required keys:
- `JSEARCH_API_KEY` — RapidAPI key for JSearch
- `ADZUNA_APP_ID` + `ADZUNA_APP_KEY` — Adzuna developer credentials
