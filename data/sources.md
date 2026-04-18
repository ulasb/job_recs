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
| Stripe | Greenhouse | Yes | stripe |
| Airbnb | Greenhouse | Yes | airbnb |
| Spotify | Lever | Yes | spotify |
| Canva | Lever | Yes | canva |
| Databricks | Greenhouse | No | databricks |
| Scale AI | Greenhouse | No | scaleai |
| Cloudflare | Greenhouse | No | cloudflare |
| Figma | Greenhouse | No | figma |
| Datadog | Greenhouse | No | datadog |

**Not yet integrated** (custom ATS, need WebSearch): Google, Microsoft, Apple, Disney, LinkedIn, Netflix, Uber, Snap, Salesforce

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

### 2026-04-10: Fifth run

**Career Page Monitor**: Checked all 10 Greenhouse/Ashby companies. 1 new role: OpenAI Head of Partner Enablement, AWS Cloud -- Go To Market department, not engineering. Filtered.

**JSearch**: 15 results across 4 queries (LA, London, Singapore, Tokyo). LA dominated by banking VP titles and small startups. London had only Field CTO and founding CTO. Singapore: defence CTO (dealbreaker), Web3 CTO (dealbreaker), intern. Tokyo: 0 results again.

**Adzuna**: London still overwhelmed by banking VP titles (10 of 15 were Citi/Citigroup/Jefferies). Singapore: mostly sales/BD roles, no qualifying engineering leadership.

**MCF**: 18 results across 2 queries. New entries all filtered: GlobalTix CTO (comp too low), BCW DLT CTO (Web3 dealbreaker), Oriental Remedies CTO (wrong domain), Peak Ocean CTO (chemical engineering), FNDR VP Eng (startup, low comp).

**WebSearch**: Found Disney VP, AI & Engineering in Burbank -- new role distinct from the previously rejected Addressable Advertising VP. Only qualifying result. Google/Waymo/OpenAI/Microsoft/Sony: no new qualifying roles. Apple: hard to parse (custom ATS).

**Key takeaway**: 1 new qualifying role (Disney VP AI & Engineering). WebFetch unavailable so could not verify posting status -- flagged as UNCERTAIN. Market continues extremely thin at this level.

### 2026-04-11: Sixth run

**Career Page Monitor**: Checked all 10 Greenhouse/Ashby companies. 0 new exec engineering roles.

**JSearch**: 10 results for LA only; London/Singapore/Tokyo all returned 0. LA results: AEG VP Eng ($217-300K, below threshold), IV.AI (small/player-coach), Disney Addressable Ads (duplicate), banking/civil eng titles, Thiozen ($180-200K). No qualifying results.

**Adzuna**: London dominated by banking VP titles again (Citi, Jefferies, Robert Walters). RELX/Elsevier reposted at £63K. Singapore: Hays confidential CTO (duplicate). No qualifying results.

**MCF**: API returning 403 Forbidden on both queries. May be blocked or rate-limited. Need to investigate.

**WebSearch**: Found Adyen VP Engineering ML/AI (Amsterdam, ~100-person team) — strong match on paper but role appears closed (Greenhouse URL returns error). Scale AI VP Enterprise surfaced but similar role was rejected prior. No new roles at any target company (Google, Apple, Microsoft, Disney, Sony, Waymo, Anthropic, OpenAI). Tokyo leads all low-comp/small-team. Exec recruiter boards (Heidrick, Riviera) have no public listings.

**Key takeaway**: Zero qualifying results. MCF API may be broken. Adyen VP Eng ML/AI was the most interesting lead but appears closed; worth monitoring for reopening.

### 2026-04-12: Seventh run

**Career Page Monitor**: Checked all 10 Greenhouse/Ashby companies. 0 new exec engineering roles.

**JSearch**: LA returned 10 results — Ghost VP Eng was misleading (B2B marketplace, not AI), Irvine Tech VP at $190-210K (below threshold), rest were small startups or wrong domains. London/Tokyo returned 0 results. Singapore timed out.

**Adzuna**: London still dominated by banking VP titles. Sonar VP Domain Leader at £108K (below threshold). Singapore: Vouch CTO (duplicate), rest were BD/sales roles.

**MCF**: API working again (was 403 yesterday). CTO query: 15 results, all previously seen or filtered. VP Eng query: 3 results, all filtered. Market consistently below comp thresholds.

**WebSearch**: Extensive search of all target companies. Google careers pages render as JavaScript — cannot verify role status via WebFetch. Sony VP Software Development returns 404 (likely filled). Waymo Director DevAI confirmed CLOSED. No new qualifying roles at OpenAI, Anthropic, Apple, Disney, Microsoft, Netflix, LinkedIn. StockX VP Eng was from Nov 2022 (stale). AlphaSense Head of Engineering Search/AI is borderline (reports to EVP, possibly too junior).

**Key takeaway**: Zero qualifying results for the fourth consecutive day. Market remains extremely thin for publicly posted exec eng roles at this level.

### 2026-04-13: Eighth run

**Career Page Monitor**: Checked all 10 Greenhouse/Ashby companies. 0 new exec engineering roles.

**JSearch**: LA returned 10 results — all duplicates (Reku SVP, AEG), below comp threshold (Irvine Tech $190-210K), wrong domain (Sompo insurance, WSP construction, PacWest Bank security), or small/player-coach (Ghost, VirtualVocations). London returned 10 — banking VP titles (JPMorgan, Goldman), sales-facing (Cloudera), consulting (ESR Healthcare). Singapore timed out. Tokyo 0 results.

**Adzuna**: London dominated by banking VP titles again (Citi, Jefferies). Sonar VP Domain Leader reposted at £108K (below threshold). Singapore: Vouch CTO and Hays CTO duplicates, rest are BD/sales/non-engineering roles.

**MCF**: CTO query returned 15 — all previously seen or filtered (low comp, Web3, chemical engineering). VP Eng query returned 2 — FNDR (small/low comp), Google Principal Architect (solutions role, not eng leadership).

**WebSearch**: Isomorphic Labs Head of Engineering London confirmed CLOSED (removed from Greenhouse board). WPP/Choreograph VP Engineering Campaign Management in London — ad-delivery domain mismatch. Zapier Sr. Director Applied AI — strong comp ($373-560K) but player/coach emphasis. No new qualifying roles at any target company. Robert Half Tokyo VP Eng is actually Engineering Manager at ¥12-18M requiring JLPT N2.

**Key takeaway**: Zero qualifying results for the fifth consecutive day. Isomorphic Labs was the most interesting near-miss but the role was filled/removed. Market remains extremely thin.

### 2026-04-13: Eighth run (re-run with expanded scope)

**Expanded scope**: Added 7 target companies (Stripe, Netflix, Uber, Airbnb, Snap, Spotify, Salesforce) and new geographies (Canada: Toronto/Vancouver/Montreal; Europe: Amsterdam, Berlin, Dublin, Zurich, Stockholm).

**New career page integrations**: Airbnb (Greenhouse, 237 jobs), Spotify (Lever, 176 jobs), Stripe (Greenhouse, 497 jobs) all working. Lever integration needed timeout fix (increased to 30s). No new exec eng roles at any of the 12 monitored companies.

**New target companies**: Netflix has 0 VP/Director roles (only EM-level). Uber, Snap have 0 relevant openings. Airbnb has 0 VP/Director roles. Spotify has 0 VP/Head roles. Stripe has 0 exec eng roles on Greenhouse. **Salesforce is the winner** — multiple VP Software Engineering roles found via WebSearch, including Agentforce Marketing (AI-first) and Revenue Cloud (Agentic platform). Salesforce career site blocks WebFetch (404 WAF) but roles are findable via site search.

**Canada**: Very thin at exec level. JSearch returned 0 for Toronto, Adzuna returned 2 (both below threshold). No VP/CTO roles at qualifying companies found via WebSearch either. API sources are not useful for Canadian exec roles.

**Continental Europe**: JSearch returned 0 for Amsterdam, Berlin, Dublin. Adzuna Germany found Intercom Senior Director Engineering Berlin — the best new find. Adzuna Netherlands returned 0. Adzuna France returned only French-language junior roles. Direct Greenhouse/Lever monitoring + WebSearch are the primary channels for European exec roles.

**Key results**: 3 qualifying roles found — Salesforce VP Agentforce Marketing (Bellevue), Intercom Senior Director Engineering (Berlin, VERIFIED OPEN), Salesforce VP Revenue Cloud (multi-location). First qualifying results in 6 days, driven by expanded company list.

### 2026-04-14: Ninth run

**Career Page Monitor**: Checked all 12 Greenhouse/Ashby/Lever companies. 0 new exec engineering roles.

**JSearch**: LA returned 10 — below comp threshold (AEG $217-300K, Irvine Tech $190-210K, PacWest $121-200K), wrong domains (Sompo insurance, construction), player-coach roles, duplicates. London returned 10 — banking VP titles (JPMorgan, Citi, Goldman Sachs, Jefferies), sales-facing (Cloudera), ad delivery (WPP). Singapore returned 10 — crypto/blockchain dealbreaker (3 roles), requires Chinese fluency (OSW), Field CTO (Circles). Tokyo returned 0.

**Adzuna**: London dominated by banking VP titles again. RELX reposted at £63K, Sonar VP Domain Leader at £108K (both below threshold). Singapore: sales/BD roles, Vouch CTO and Hays CTO duplicates.

**MCF**: CTO query timed out. VP Eng returned 2 — FNDR VP Eng at SGD 5,500-20K/mo (below threshold, tiny startup), Google Principal Architect (solutions role).

**WebSearch**: Disney VP Software Engineering (Glendale, $305-409K) is specifically Addressable Advertising — ad-delivery domain mismatch per learned preferences. Mastercard VP Software Engineering London confirmed CLOSED. Apple Sr. Director ML Engineering & Innovation REMOVED from careers site. No new roles at Google, Microsoft, Sony, Netflix, Uber, Snap, LinkedIn, Anthropic, OpenAI, Waymo, Stripe, Airbnb, Spotify. Greenhouse/Lever boards all small companies or crypto. Exec recruiters have no public listings.

**Key takeaway**: Zero qualifying results for the sixth consecutive day. Disney VP Addressable Advertising was the only new role at a target company but domain is a mismatch. Market continues extremely thin for publicly posted exec eng roles at this level.

### 2026-04-18: Eleventh run

**Career Page Monitor**: Waymo posted new **Director of Engineering, London Site Lead** (Simulator Team). £230-242K GBP base. ML/sim-focused. Verified OPEN. First qualifying result from the career monitor in multiple runs.

**JSearch**: LA/London/Singapore repeated the usual noise (banking VPs, staffing, sales-facing, crypto dealbreakers, small startups). Tokyo returned 0 as always.

**Adzuna**: UK dominated again by banking VPs and sub-£160K postings. AU CTO query surfaced Latitude IT (57 employees — rejected prior). DE returned only 2 (Aiven AE, Affinidi — rejected prior).

**MCF**: All Singapore results previously seen/filtered. FNDR VP Eng repeated.

**WebSearch**: No new exec eng roles at any target company beyond Waymo. Salesforce surfaced but in SRE/India. Tokyo market unchanged (SyntheticGestalt still the only lead, seen prior).

**Key takeaway**: 1 qualifying role (Waymo Director of Engineering, London Site Lead). Career monitor continues to be the highest-signal source — the only channel that produced a hit today. All other channels continue to repeat the same noise.

### 2026-04-15: Tenth run (first Australia/NZ inclusion)

**New geographies**: Added Australia and New Zealand to target locations (Sydney, Melbourne, and NZ cities). Searched Adzuna AU/NZ and did WebSearch for Australian tech companies.

**Career Page Monitor**: 0 new exec eng roles across all 12 monitored companies.

**Adzuna AU**: VP engineering query returned only 2 results (wrong level/domain). CTO query returned 15 results — mostly recruiter postings for confidential clients, small companies, or non-engineering. Adzuna NZ returned 0 results.

**WebSearch Australia**: Much more productive than API sources. Found Canva Engineering Director - AI Platform (ANZ Remote) — first qualifying AU role. Canva uses Lever (jobs.lever.co/canva), same ATS integration already built for Spotify.

**Optiver Head of Infrastructure (APAC) Sydney**: verified OPEN but filtered — player-coach + SRE/infra domain.

**Atlassian**: Main exec eng role (Head of Engineering DX) is in Salt Lake City, not Sydney. Custom careers site, not in career monitor.

**Key takeaway**: 1 qualifying result (Canva Engineering Director - AI Platform, ANZ Remote). Australia broadens the target significantly. Recommend adding Canva to career page monitor (Lever slug: `canva`).

**Action items**:
1. ✅ Added Canva to `scripts/monitor_careers.py` — turns out Canva uses SmartRecruiters (not Lever), so added new SmartRecruiters fetcher function. Slug: `Canva` (case-sensitive). 300 jobs on board.
2. Investigate Atlassian's custom ATS for future monitoring
3. Continue including Australia in Adzuna searches despite low yield — WebSearch is primary channel
4. **Link verification learning**: Canva AI Platform Director URL appeared valid in WebSearch but returned "Page Not Found" when user clicked through. Same pattern as Salesforce URLs. For future runs, WebFetch error on primary ATS URL = drop the role. Only present if primary ATS URL loads cleanly.
