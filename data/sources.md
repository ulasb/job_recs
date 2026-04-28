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

### 2026-04-28: Seventeenth run

**Career Page Monitor**: 13 companies checked. 0 new exec engineering roles.

**JSearch**: 38 results across LA/London/SG/Remote-AI/Tokyo. Same patterns. LA dominated by Reku duplicates, IV.AI duplicates, Voyager (defense), Pinterest VP Ads Quality (duplicate of Seattle posting from 2026-04-26 with location "Remote"), Everest Search supply chain, Thiozen, Hadrian. London entirely banking VPs (BNY Mellon multi, Citi multi, JPMorgan, State Street, "Professional" recruiter postings) plus Aisel Health duplicate. Singapore: BCW DLT (Web3), Field CTO Circles, Krisvconsulting crypto, OSW Global CTO (Chinese-fluency duplicate), Libeara (Web3), Argyll Scott recruiter, Page Executive confidential, NodeFlair/Peak Ocean/Oriental Remedies duplicates. Remote-AI: Duck Creek (insurance), Impiricus (small), ClosedWon (small), League $258-322K (below comp), FutureFeed (cyber/compliance — out of scope), Lincoln Financial (PM), Axos Bank (banking IT), Quickswoop (opaque). Tokyo 0 results as usual.

**Adzuna**: London VP Eng — 15 results, banking VPs (Citi/Citigroup/JPMorgan multi) and sub-£160K (Apogee £82K duplicate, Sanogenetics £120-150K, Stanford Black £108K, Snowflake EMEA Sales £49K, Malt SEM £79K, Portfolio Group £150K duplicate). London Head of Eng — all sub-£160K (Harrington Starr £118-119K multi, Tria Recruitment £95K, ASA £70-75K, Keyrock £87K crypto, Resource Group £78K duplicate, S&P Detection Eng £73-80K, Barclays £59K, La Fosse interim £75K). Singapore: Hays AI Security (out of scope), Ceffu (crypto), UOB Infra IC (banking), Evo Commerce duplicate.

**MCF**: All previously seen (NodeFlair, GlobalTix, Kaneze, ChemOne, Custera, Vocalbeats, Libeara, Randstad, ST Engineering, Cloudflare Solutions, Eversafe, FNDR — duplicates or below comp). Codex Solutions CTO new but SGD 13-23K/mo (below threshold).

**WebSearch**: **SERVICE OUTAGE.** All WebSearch and WebFetch calls returned `Prompt is too long` or `529 Overloaded` for the entire run, including from minimal-context sub-agents. Confirmed reproducible. Target-company exec-eng research (Google, Apple, Microsoft, Salesforce, LinkedIn, Pinterest, Disney/Sony/Netflix/Uber/Snap, Tokyo English boards, London exec, Heidrick public boards) could not be performed. One-day backfill required next run.

**Key takeaway**: 0 qualifying roles. WebSearch outage is the major caveat — given that Google/Apple/Pinterest finds in the past three runs all came via direct google.com/apple.com indexing, today's API-only sweep was always going to be thin. Re-attempt WebSearch coverage tomorrow.

### 2026-04-27: Sixteenth run

**Career Page Monitor**: 13 companies checked. **1 new exec engineering role**:
  - **Spotify Director of Engineering, Experience** (Stockholm) — owns Engineering for "Identity & Investment" product area in Consumer Experience Mission, ~70-engineer org, core consumer experience across iOS/Android, target-company + target-city. Per Spotify's published ladder, Director on the EM track maps to L8. First qualifying career-monitor hit since Waymo London on 2026-04-18.

**JSearch**: ~50 results across LA/London/SG/Remote-AI/Tokyo. Same patterns: LA dominated by Hadrian (hardware), OakTree Data Eng SVP, Jobot Network Eng Leader sub-$300K, Canonical distributed open-source. London = banking VPs (BNY Mellon multi, Citi multi) + Aisel Health early-stage. Singapore = Page Executive confidential, Accelcia blockchain (Web3 dealbreaker), NodeFlair/OSW duplicates. Remote-AI: FedEx Manager (below level), Relativity Space $245-336K (below comp), small startups. Tokyo 0 results as usual.

**Adzuna**: London VP Eng — 15 results, all sub-£160K (Stanford Black £108K, Citi £85K, Snowflake EMEA Sales £49K, Malt Senior EM £79K, Malt Director £60K) or banking VPs or sales-facing. London Head of Eng — all sub-£160K (Portfolio Group £150K Castle Baynard, La Fosse interim £75K, RF Maintenance £73K, Tech4 sub-£70K, trg Principal £105K). Singapore: only UOB VP Infrastructure Engineer IC (banking infra, filtered).

**MCF**: All previously seen Singapore CTOs (NodeFlair, ChemOne $18-20K SGD/mo, FNDR, APSN exec assistant, Eversafe AI Eng IC role).

**WebSearch**: **Two qualifying roles**:
  1. **Apple Director of Personalization, Apple Intelligence** (Cupertino) — $305-487K base, leads multidisciplinary teams across UI/ML/Infra defining personalized OS experiences for Apple Intelligence. Closes 2026-05-27. Verified OPEN via evenbreak.com mirror (jobs.apple.com is JS-rendered, blocks direct WebFetch). First Apple exec eng find of the project. Apple Director maps to L8-equivalent per learned prefs.
  2. **Google Senior Director, Engineering, Merchant Shopping** ($349-485K, MTV/Reston/Atlanta) — Multi-year roadmap for Google Merchant Center, includes GenAI for merchants (Product Studio). UNCERTAIN due to Google JS rendering; cross-verified via independent WebSearch indexing.

Filtered Google roles (out of scope per learned prefs): VP Cloud Protection (security), Sr Dir Hybrid/On-Premise Infra Cloud (infra), Sr Dir Infrastructure Solutions Cloud (infra), Sr Dir GCE Core Virtualization (systems), Sr Dir Data Integration (data eng). Previously presented and still open: Sr Dir Geo Maker, Sr Dir Ecosystem Growth, Sr Dir Emerging Agents Applied AI, VP Workspace Drive — all surfaced again on WebSearch but already in seen_jobs.

Disney VP Software Eng Glendale = previously-rejected Addressable Advertising role. Sony Sr Dir Data Platform Eng = data eng (out of scope). No new exec roles at Microsoft, Pinterest, Snap, LinkedIn, Anthropic, OpenAI, Waymo, Stripe, Airbnb, Uber, Salesforce. Tokyo unchanged.

**Verification learning**: evenbreak.com (UK accessible-employer feed) mirrored the Apple posting cleanly with full salary + closing date — useful fallback when Apple's JS-rendered ATS blocks WebFetch. Worth checking for future Apple roles.

**Key takeaway**: 3 qualifying roles, all at distinct named target companies (Apple, Spotify, Google) — first three-target-company day in the project. Apple Director of Personalization is the strongest single match (exact AI/ML + personalization domain, fresh posting, leader-of-leaders scope, explicit close date). Spotify Stockholm reactivates the European-target pipeline.

### 2026-04-26: Fifteenth run

**Career Page Monitor**: 13 companies checked. 0 new exec engineering roles.

**JSearch**: ~40 results across LA/London/SG/Remote/Tokyo. LA dominated by IV.AI duplicates, AEG, civil/mechanical/plumbing engineering (WSP), Voyager Technologies (defense), Hadrian (hardware), Pinterest VP Ads Quality (followed up via WebSearch — see below), Genpact AVP. London: BNY Mellon multiple, Citi multiple, State Street, Aisel Health duplicate, BlackRock solutions/sales. Singapore: Big-Foot, Peak Ocean (chemical), Manpower, Talent Titans, Libeara, Custera, Argyll Scott, Oriental Remedies, OSW (Chinese-fluency duplicate), Cognition (Field CTO duplicate). Remote-AI: ClosedWon, Duck Creek (insurance), ScienceLogic (rejected prior), Jobgether $100-125K, Hexion, Jack & Jill aggregator, SitusAMC $100-160K, Tango. Tokyo 0 results.

**Adzuna**: London VP eng — banking VP titles (JPMorgan, Citi multiple) and sub-£160K (Apogee £82K, Portfolio Group CTO £150K, Stanford Black £108K, Snowflake £49K, Malt £80K). London Head of Eng — all sub-£120K (Walker Cole, Resource Group, ASA, Ec1, S&P Detection Eng, Keyrock crypto £88K, Barclays £59K, ih Smart Home Installer, trg Principal Eng £105K, Portfolio Group £150K, Uber Boat electrical, CV Consulting maintenance). SG: Techtanium CTO (no comp), Civils.ai full-stack, TE Connectivity Staff Eng, Oliver James VP Tech Strategy (recruiter), Atomatic Operations, Dell Associate, Newbridge sales, Elastic pre-sales, NCS AI Architect, Xendit AM, Mastercard Director TPM (PM). All filtered.

**MCF**: All previously seen Singapore CTOs (NodeFlair, GlobalTix, Kaneze, Randstad, Libeara, Vocalbeats SGD 40-45K but small, Custera, ChemOne, Peak Ocean, ST Engineering ×2 below comp, Cloudflare Solutions). FNDR VP Eng duplicate.

**WebSearch**: **Two qualifying roles**:
  1. **Pinterest VP, Ads Quality Engineering** — Seattle/SF/Palo Alto/LA hybrid, $400–485K base + RSU. Lead 200+ AI/ML eng on monetization quality/relevance — STRONG domain bullseye for user's Google Ads Understanding background. Verified via LinkedIn (`linkedin.com/jobs/view/4404922421`); aggregators (pitchmeai, theladders) showed misleading $200–250K range. Posted 3 days ago. **First qualifying non-Google role in many runs.**
  2. **Google Senior Director, Engineering, Google Design Platform** — Mountain View, $349–485K base + bonus + equity. Lead ~130-person eng org across multiple geographies on design system/components, includes AI-for-design (genUX, design-to-code, design agents). Indexed on google.com/about/careers; flagged UNCERTAIN due to JS-rendering verification limit.

Filtered Google roles (out of scope): VP Silicon Eng (hardware), VP Cloud Protection (security), VP Eng Finance/Compliance/Governance (corporate IT — matches Databricks rejection), Sr Dir Data Integration (data eng — out of scope), Sr Dir AI Platform Cloud Security (security), Sr Dir ML Compiler (IC-adjacent), Sr Dir GCE Core Virtualization (systems), Sr Dir Hybrid/On-Premise Infra Cloud, Sr Dir Infra Solutions Cloud (infra), Sr Dir Platform Operations GDC (SRE-adjacent). **Google Sr Dir ML Developer Experience CONFIRMED CLOSED** today (page returns "Job not found. This job may have been taken down").

No new qualifying roles at any other target company (Microsoft, Apple, Disney, Sony, Netflix, Anthropic, OpenAI, Waymo, Stripe, Airbnb, Spotify, Uber, Snap, Salesforce, LinkedIn). Tokyo unchanged.

**Key takeaway**: 2 qualifying roles. Pinterest VP Ads Quality is the most exciting non-Google find in many runs — exact domain match (ads ML/quality vs ad-delivery), strong scope (200+ engineers), comp clears threshold, target-tier consumer-tech employer. Reminder: aggregator salary ranges should be cross-verified on LinkedIn for US Ads/AI roles before filtering.

### 2026-04-25: Fourteenth run

**Career Page Monitor**: 13 companies checked. 0 new exec engineering roles.

**JSearch**: ~50 results across LA/London/SG/Remote/Tokyo. LA dominated by IV.AI duplicates, AEG, civil/mechanical engineering (WSP, Infrastructure Engineering Inc), Voyager Technologies (defense — dealbreaker), Hadrian (hardware), Stem (below comp). London entirely banking VP titles (BNY Mellon multiple, Citi multiple, State Street, BlackRock + solutions/sales-facing). Singapore: confidential CTO/COO, recruiter postings (Talent Titans, Argyll Scott, Page Executive), petrochemical (Peak Ocean), small (Big-Foot), Web3/Libeara, OSW (Chinese-fluency req duplicate). Remote-AI: HPE program mgmt (PM not eng), CrowdStrike Sr Dir AI ($210-300K below), Granicus internal AI ($169-229K below), Carthage assistant role, IQVIA learning enablement, Jobgether BD/alliances, Dana-Farber healthcare, Adonis healthcare-small. Tokyo 0 results.

**Adzuna**: London (30 results across two queries) all banking VPs (Citi, JPMorgan, Barclays) or below £160K (Apogee £82K, Resource Group £78K, Portfolio Group £150K, Keyrock crypto £88K, Walker Cole pharma, RF Recruitment £74K) or domain mismatches (electrical, BESS, pharmaceutical). Singapore: Ceffu (crypto), UOB (banking IC), Evo Commerce (small CPG).

**MCF**: All Singapore results previously seen (NodeFlair, GlobalTix, Kaneze, Custera, Libeara, Vocalbeats, Randstad, FNDR) or below comp thresholds. ST Engineering (defense), Cloudflare Solutions Architect filtered.

**WebSearch**: **Three new qualifying roles at Google** via direct google.com/about/careers indexing:
  1. **VP, Workspace Drive** — $550K base, Sunnyvale/Boulder/NYC. 2B users, GenAI/Agentic AI/RAG focus, lead 300+ engineers. Strongest single-day match in any run. Application open until at least 2026-04-22.
  2. **Senior Director, Engineering, Geo Maker** — Mountain View/Sunnyvale. Maps/Earth/BigQuery Analytics with GenAI-forward solutions. Strong consumer-tech + location-intelligence match (user has Foursquare VP Eng background).
  3. **Senior Director, Engineering, Ecosystem Growth** — Sunnyvale/Kirkland/Tel Aviv. Sharing/Connection/Ecosystem Journeys/Growth — full-stack consumer infra. Strong match.

Filtered Google roles (out of scope per learned prefs): VP Cloud Protection (security), Sr Dir ML Compiler (IC-adjacent), Sr Dir GCE Core Virtualization (systems eng), Sr Dir Data Center R&D (hardware), Sr Dir Hybrid/On-Premise Infra Cloud (borderline infra), Sr Dir Infrastructure Solutions Cloud (borderline infra), Sr Dir Platform Operations GDC (SRE-adjacent).

No new qualifying roles at any other target company (Microsoft, Apple, Disney, Sony, Netflix, Anthropic, OpenAI, Waymo, Stripe, Airbnb, Spotify, Uber, Snap, Salesforce). Disney VP Software Engineering Glendale is the previously-rejected Addressable Advertising role. Tokyo market unchanged.

**Google verification challenge** (consistent with 2026-04-24 run): Google's careers portal is JS-rendered; WebFetch returns the search results page shell, not individual job content. Cross-verified all 3 finalists via multiple independent WebSearch queries showing consistent role descriptions indexed on google.com (not aggregators). Flagged as UNCERTAIN; user should manually click through to confirm.

**Key takeaway**: 3 qualifying roles, all at Google. Second consecutive day with multiple Google finds — direct WebSearch against google.com/about/careers continues to be the highest-signal channel for this profile. The VP, Workspace Drive role is the strongest single match in any run to date (exact title, $550K base, target company, 2B-user consumer scope, GenAI focus, 300+ eng team).

### 2026-04-24: Thirteenth run

**Career Page Monitor**: 13 companies checked. 2 new roles — Anthropic "Head of ANZ, Applied AI" (Sydney, verified Field CTO/pre-sales — filtered per learned prefs) and Airbnb "Head of Fundraising, Airbnb.org" (non-eng — filtered).

**JSearch**: 40 results across LA/London/SG/Remote-AI/Tokyo. Usual pattern — LA dominated by banking/construction/hardware VPs, London by banking VP titles (BNY Mellon, State Street, Black Rock, JPMorgan, Citi, Jefferies), SG by confidential recruiter CTOs and Field CTO (Cognition) + crypto dealbreakers, Remote by below-threshold aggregator postings (Jobgether, Hexion, SitusAMC, Refinitiv). Tokyo 0 results as usual.

**Adzuna**: London VP + Head of Eng (30 results) all below £160K or banking/staffing/non-eng. SG returned 2 (Ceffu crypto, UOB Infra IC).

**MCF**: 15 + 1 results. Vocalbeats.AI new (SGD 40-45K/mo) but 51-200 employees — likely too small. Rest duplicates or below threshold.

**WebSearch**: **Two qualifying roles found at Google** via direct google.com/about/careers indexing:
  1. **Senior Engineering Director, AI Data Infrastructure** — $365-505K base, Mountain View, AI/ML infra, likely L8+/L9. Strong match.
  2. **Senior Director, Engineering, Emerging Agents, Applied AI** — Google Senior Director band, Mountain View, GenAI agents for customer-interaction applications. Strong match.

Disney VP Software Engineering Glendale reconfirmed as Addressable Advertising (duplicate reject). Waymo Director Simulation Evaluation CLOSED. SyntheticGestalt VP Eng Tokyo not accepting applications. ScienceLogic VP Skylar AI — not target, comp uncertain, ~500 employees.

**Google verification challenge**: Google's careers portal is JS-rendered; WebFetch returns the page shell but cannot parse individual job content. Cross-verified via multiple independent WebSearch queries showing consistent role descriptions indexed on google.com (not aggregators). Flagged as UNCERTAIN via WebFetch; user should manually click through to confirm.

**Key takeaway**: 2 qualifying roles, both at Google — first Google finds in over a week. WebSearch across target-company domains remains the highest-signal channel for roles not on Greenhouse/Ashby/Lever.

### 2026-04-19: Twelfth run

**Career Page Monitor**: 13 companies checked. 0 new exec engineering roles.

**JSearch**: 38 results across LA/London/Singapore/Remote-AI/Tokyo. LA dominated by banking VPs (BlackRock, Citi, JPMorgan, Goldman) and sub-$350K roles at WSP (civil), PTR Global (aerospace), Pacific Western Bank (security), Stem ($250-300K), VirtualVocations (preconstruction). London: JPMorgan Markets CRM VP, Elsevier reposted, BNY Mellon SVP Full-Stack, Aisel Health. SG: all confidential/recruiter CTOs, Global CTO at OSW (previously rejected Chinese req), National-Security CTO (defense). Tokyo: 0 results as usual.

**Adzuna**: London VP Eng + Head of Eng queries returned 30 results, all below £160K or staffing/recruiter postings (Portfolio Group £150K, Reed £120-150K, RF Recruitment £74K, Edison Smart £70K, TEC Partners £69K, Velocity Tech £83K, Bupa OH £68K, PSR Solutions £110-120K, techUK £60K, Grant Thornton £63K). Sydney VP Eng: 0 results.

**MCF**: CTO query returned 15 results (all below SGD 25K threshold or previously seen — NodeFlair, GlobalTix, Kaneze, ChemOne, Oriental Remedies, Peak Ocean, Randstad). VP Eng returned 1 (FNDR, duplicate).

**WebSearch**: All target companies checked. Disney VP Software Engineering in Glendale confirmed via WebFetch as previously-seen Addressable Advertising role (ad-delivery domain mismatch). Waymo Developer AI confirmed CLOSED. Waymo London Site Lead already seen (yesterday). No new roles at OpenAI, Anthropic, Apple, Microsoft, Disney, Sony, Netflix, Stripe, Airbnb, Uber, Snap, Spotify, Salesforce, LinkedIn. Europe/Canada/Tokyo markets unchanged.

**Key takeaway**: Zero qualifying results. Market continues extremely thin at this level. Career monitor remains highest-signal source — Waymo London was the last hit and is now seen. Most large-company exec roles likely filled via retained search firms that don't post publicly.

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
