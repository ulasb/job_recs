# Job Sources Configuration

Last updated: 2026-04-06

## API Sources

### Indeed (MCP Integration)
- **Type**: Direct MCP tool (`mcp__claude_ai_Indeed__search_jobs`)
- **Coverage**: US primary, some international
- **Auth**: Handled by MCP
- **Notes**: Primary structured source. Also provides `get_job_details`, `get_company_data`, `get_resume`.
- **Queries**: Derived from user profile — run one search per (title, location) combination.

### JSearch (Google for Jobs via RapidAPI)
- **Type**: REST API via `scripts/search.py --source jsearch`
- **Endpoint**: `https://jsearch.p.rapidapi.com/search`
- **Coverage**: Global — aggregates Google for Jobs (LinkedIn, Glassdoor, ZipRecruiter, employer sites)
- **Auth**: RapidAPI key (`JSEARCH_API_KEY`)
- **Rate Limit**: Free tier ~200 req/month, paid ~$30/mo for more
- **Notes**: Best single source for broad coverage. Captures LinkedIn postings without needing LinkedIn API.

### Adzuna
- **Type**: REST API via `scripts/search.py --source adzuna`
- **Endpoint**: `https://api.adzuna.com/v1/api/jobs/{country}/search/{page}`
- **Coverage**: 16 countries — strong in UK, EU, Australia, Singapore
- **Auth**: App ID + App Key (`ADZUNA_APP_ID`, `ADZUNA_APP_KEY`)
- **Countries**: au, at, br, ca, de, fr, gb, in, it, nl, nz, pl, ru, sg, us, za
- **Notes**: Best structured source for European and Singapore jobs.

### RemoteOK
- **Type**: REST API via `scripts/search.py --source remoteok`
- **Endpoint**: `https://remoteok.com/api`
- **Coverage**: Global remote jobs, ~30K listings
- **Auth**: None
- **Notes**: No auth needed. Returns JSON directly. Tech/remote focused.

### Arbeitnow
- **Type**: REST API via `scripts/search.py --source arbeitnow`
- **Endpoint**: `https://www.arbeitnow.com/api/job-board-api`
- **Coverage**: EU-focused, ATS-sourced
- **Auth**: None
- **Notes**: Good for European positions, especially DACH region.

### Himalayas
- **Type**: REST API via `scripts/search.py --source himalayas`
- **Endpoint**: `https://himalayas.app/jobs/api`
- **Coverage**: Remote jobs with timezone filtering
- **Auth**: None
- **Notes**: Useful for finding remote roles compatible with specific timezone windows (e.g., Asia-friendly hours).

### MyCareersFuture (Singapore)
- **Type**: REST API via `scripts/search.py --source mycareersfuture`
- **Endpoint**: `https://api.mycareersfuture.gov.sg/v2/jobs`
- **Coverage**: Singapore only
- **Auth**: None
- **Notes**: Government-backed, comprehensive Singapore coverage.

## Target Company Career Pages (via `scripts/monitor_careers.py`)

These are checked via structured JSON APIs (Greenhouse/Ashby). The monitor filters for VP/Director/Head/CTO-level engineering titles.

| Company | ATS | Target? | Slug |
|---------|-----|---------|------|
| Anthropic | Greenhouse | Yes | anthropic |
| OpenAI | Ashby | Yes | openai |
| Waymo | Greenhouse | Yes | waymo |
| Sony Interactive | Greenhouse | Yes | sonyinteractiveentertainmentglobal |
| Stripe | Greenhouse | No | stripe |
| Databricks | Greenhouse | No | databricks |
| Scale AI | Greenhouse | No | scaleai |
| Cloudflare | Greenhouse | No | cloudflare |
| Figma | Greenhouse | No | figma |
| Datadog | Greenhouse | No | datadog |

**Not yet integrated** (custom ATS, need WebSearch): Google, Microsoft, Apple, Disney, LinkedIn, Netflix

## Executive Recruiter Public Boards

Checked via WebSearch/WebFetch. Most top firms (Spencer Stuart, Russell Reynolds, Egon Zehnder) don't post publicly.

| Firm | URL | Notes |
|------|-----|-------|
| Heidrick & Struggles | heidrick.com/open-roles | Public, HTML, JS-rendered |
| True Search | truesearch.com/searches | Tech-focused, some listings public |
| Riviera Partners | rivierapartners.com/opportunities | Tech exec roles, public |

## Web Sources (searched via WebSearch + WebFetch)

These sources lack APIs. Search them using WebSearch with site-specific queries.

### Japan
| Board | URL | Query Pattern | Notes |
|-------|-----|---------------|-------|
| GaijinPot | gaijinpot.com/work | `site:gaijinpot.com/work {query}` | English-language jobs in Japan |
| Daijob | daijob.com | `site:daijob.com {query}` | Bilingual jobs in Japan |
| CareerCross | careercross.com | `site:careercross.com {query}` | Bilingual professional jobs |
| Wantedly | wantedly.com | `site:wantedly.com {query} japan` | Startup/tech focused |
| TokyoDev | tokyodev.com | `site:tokyodev.com {query}` | Developer jobs in Japan |

### South Korea
| Board | URL | Query Pattern | Notes |
|-------|-----|---------------|-------|
| Saramin | saramin.co.kr | `site:saramin.co.kr {query}` | Dominant Korean job board |
| JobKorea | jobkorea.co.kr | `site:jobkorea.co.kr {query}` | Major Korean job board |
| Wanted | wanted.co.kr | `site:wanted.co.kr {query}` | Tech-focused Korean board |

### Thailand
| Board | URL | Query Pattern | Notes |
|-------|-----|---------------|-------|
| JobThai | jobthai.com | `site:jobthai.com {query}` | Dominant Thai job board |
| JobsDB Thailand | th.jobsdb.com | `site:th.jobsdb.com {query}` | Regional board (SEEK) |

### General
| Board | URL | Query Pattern | Notes |
|-------|-----|---------------|-------|
| Company career pages | varies | `{company} careers {title}` | Direct employer postings |
| AngelList/Wellfound | wellfound.com | `site:wellfound.com {query}` | Startup jobs globally |

## Crawl Learnings

_Updated after each run._

### 2026-04-06: First run

**Indeed MCP**: Poor for executive-level roles. Returned mostly irrelevant results (sales roles, wrong titles). VP/CTO/Head searches at this seniority level return very few hits. Consider deprioritizing for this user profile.

**JSearch**: Best structured API source. Found 4 relevant results including Cognition (Singapore) and SERIOUS AI (Remote). However, returned 0 results for Tokyo and Seoul — coverage in Asia is weak for English-language executive roles.

**Adzuna**: Good for UK VP roles (found Elsevier, Infinit, Aisel Health). However, many false positives from banking "VP" titles (Citi/Citigroup — "VP" is a banking level, not a functional title). Singapore search returned 0 results. Add filtering for banking VP titles in future.

**RemoteOK**: No executive-level roles at all. The platform skews heavily junior/mid-level. Consider removing from searches for this profile or only using with very specific queries.

**Arbeitnow**: EU-focused but returned only junior/mid-level roles. No executive matches. Same as RemoteOK — not useful for this seniority level.

**Himalayas**: Same issue — no executive-level matches despite fetching 500 listings. Platform skews junior/mid.

**MyCareersFuture**: Good for Singapore CTO roles — found 3 relevant results (NodeFlair CTO, Kaneze AI CTO, Randstad CTO). However, comp levels for Singapore roles were consistently below target.

**WebSearch**: Essential for Tokyo jobs (found SyntheticGestalt VP Eng). Also found UK proptech and Tes VP Eng. However, some results were stale (2024 listings surfaced as current). Need to verify recency.

**Key takeaway**: For this seniority level, JSearch + Adzuna (UK) + MCF (Singapore) + WebSearch are the useful sources. RemoteOK, Arbeitnow, and Himalayas should be deprioritized or dropped. Indeed MCP is weak. WebSearch is critical for Asia.

**Action items for next run**:
1. Add a link verification step (WebFetch the job URL to confirm it's still live)
2. Filter out banking "VP" titles from Adzuna results
3. Skip RemoteOK/Arbeitnow/Himalayas for executive searches
4. Focus WebSearch on Glassdoor, LinkedIn snippets, and targeted job boards
5. Add levels.fyi as a source for verifying comp ranges at target companies

### 2026-04-09: Fourth run

**Career Page Monitor**: Checked all 10 Greenhouse/Ashby companies. Only 1 new role: Datadog Director of Product Management (AI Observability) — PM not eng, filtered. Waymo Director of Engineering (Developer AI) from prior run is now closed.

**JSearch**: 50 results across 5 queries. Massive noise — dominated by banking VP titles, data engineering roles, small startups, and wrong domains. No qualifying results.

**Adzuna**: London results almost entirely banking VP titles (Citi/Citigroup). Singapore had one opaque CTO via Vouch Recruitment (GPU infra, company hidden). No qualifying results.

**MCF**: 18 results. All below comp threshold, tiny companies, wrong domains, or previously seen.

**WebSearch**: 11 targeted queries. No new qualifying roles at any target company. Apple filled VP of AI (Amar Subramanya). Waymo Director Developer AI closed.

**Key takeaway**: Zero qualifying results. Market is extremely thin for publicly posted exec eng roles at this level. Career page monitor remains highest-signal source.
