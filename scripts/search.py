#!/usr/bin/env python3
"""Unified job search script for non-MCP API sources.

Usage:
    python3 scripts/search.py --source <source> --query <query> [--location <loc>] [--country <cc>] [--limit <n>]
    python3 scripts/search.py --source all --query <query> [--location <loc>] [--country <cc>]

Sources: jsearch, adzuna, remoteok, arbeitnow, himalayas, mycareersfuture
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime
from pathlib import Path

try:
    import certifi
    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL_CONTEXT = ssl.create_default_context()
    SSL_CONTEXT.check_hostname = False
    SSL_CONTEXT.verify_mode = ssl.CERT_NONE


def safe_date(value) -> str:
    """Convert various date formats to YYYY-MM-DD string."""
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value).strftime("%Y-%m-%d")
        except (OSError, ValueError):
            return ""
    if isinstance(value, str):
        return value[:10]
    return ""


def normalize_dedup_key(company: str, title: str, location: str) -> str:
    """Create a normalized dedup key from company, title, location."""
    def norm(s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r'[^\w\s]', '', s)
        s = re.sub(r'\s+', '_', s)
        return s
    return f"{norm(company)}|{norm(title)}|{norm(location)}"


def api_get(url: str, headers: dict = None, timeout: int = 30) -> dict:
    """Make a GET request and return parsed JSON."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        print(json.dumps({"error": f"HTTP {e.code}: {e.reason}", "body": body[:500], "url": url}), file=sys.stderr)
        return None
    except urllib.error.URLError as e:
        print(json.dumps({"error": str(e.reason), "url": url}), file=sys.stderr)
        return None


def load_env():
    """Load .env file from project root."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())


# ---------------------------------------------------------------------------
# Source adapters — each returns a list of normalized job dicts
# ---------------------------------------------------------------------------

def search_jsearch(query: str, location: str = "", country: str = "us", limit: int = 20) -> list:
    api_key = os.environ.get("JSEARCH_API_KEY")
    if not api_key:
        print('{"error": "JSEARCH_API_KEY not set in .env"}', file=sys.stderr)
        return []

    search_query = f"{query} in {location}" if location else query
    params = urllib.parse.urlencode({
        "query": search_query,
        "num_pages": 1,
        "date_posted": "week",
        "country": country.lower(),
    })
    url = f"https://jsearch.p.rapidapi.com/search?{params}"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    data = api_get(url, headers)
    if not data or "data" not in data:
        return []

    jobs = []
    for item in data["data"][:limit]:
        company = item.get("employer_name", "Unknown")
        title = item.get("job_title", "Unknown")
        loc = item.get("job_city", "")
        if item.get("job_state"):
            loc = f"{loc}, {item['job_state']}" if loc else item["job_state"]
        if item.get("job_country"):
            loc = f"{loc}, {item['job_country']}" if loc else item["job_country"]
        loc = loc or "Remote"

        salary_min = item.get("job_min_salary")
        salary_max = item.get("job_max_salary")
        salary = ""
        if salary_min and salary_max:
            salary = f"${salary_min:,.0f}-${salary_max:,.0f}"
        elif salary_min:
            salary = f"${salary_min:,.0f}+"

        jobs.append({
            "id": f"jsearch_{item.get('job_id', '')}",
            "source": "jsearch",
            "title": title,
            "company": company,
            "location": loc,
            "url": item.get("job_apply_link") or item.get("job_google_link", ""),
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "date_posted": safe_date(item.get("job_posted_at_datetime_utc")),
            "salary": salary,
            "summary": (item.get("job_description", ""))[:500],
            "job_type": item.get("job_employment_type", ""),
            "is_remote": item.get("job_is_remote", False),
            "dedup_key": normalize_dedup_key(company, title, loc),
        })
    return jobs


def search_adzuna(query: str, location: str = "", country: str = "gb", limit: int = 20) -> list:
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        print('{"error": "ADZUNA_APP_ID/ADZUNA_APP_KEY not set in .env"}', file=sys.stderr)
        return []

    params = urllib.parse.urlencode({
        "app_id": app_id,
        "app_key": app_key,
        "results_per_page": min(limit, 50),
        "what": query,
        "where": location,
        "max_days_old": 7,
        "content-type": "application/json",
    })
    url = f"https://api.adzuna.com/v1/api/jobs/{country.lower()}/search/1?{params}"

    data = api_get(url)
    if not data or "results" not in data:
        return []

    jobs = []
    for item in data["results"][:limit]:
        company = item.get("company", {}).get("display_name", "Unknown")
        title = item.get("title", "Unknown")
        loc = item.get("location", {}).get("display_name", "Unknown")

        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")
        salary = ""
        if salary_min and salary_max:
            salary = f"{salary_min:,.0f}-{salary_max:,.0f}"
        elif salary_min:
            salary = f"{salary_min:,.0f}+"

        jobs.append({
            "id": f"adzuna_{item.get('id', '')}",
            "source": "adzuna",
            "title": title,
            "company": company,
            "location": loc,
            "url": item.get("redirect_url", ""),
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "date_posted": safe_date(item.get("created")),
            "salary": salary,
            "summary": (item.get("description", ""))[:500],
            "dedup_key": normalize_dedup_key(company, title, loc),
        })
    return jobs


def search_remoteok(query: str, **kwargs) -> list:
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "JobRecsBot/1.0"}

    data = api_get(url, headers)
    if not data or not isinstance(data, list):
        return []

    # First element is metadata, skip it
    listings = data[1:] if len(data) > 1 else []
    query_lower = query.lower()
    query_terms = query_lower.split()

    jobs = []
    for item in listings:
        title = item.get("position", "")
        company = item.get("company", "Unknown")
        tags = [t.lower() for t in item.get("tags", [])]
        description = item.get("description", "").lower()

        # Basic relevance filtering
        searchable = f"{title} {company} {' '.join(tags)} {description}".lower()
        if not any(term in searchable for term in query_terms):
            continue

        loc = item.get("location", "Remote") or "Remote"
        salary_min = item.get("salary_min")
        salary_max = item.get("salary_max")
        salary = ""
        if salary_min and salary_max:
            salary = f"${int(salary_min):,}-${int(salary_max):,}"

        jobs.append({
            "id": f"remoteok_{item.get('id', '')}",
            "source": "remoteok",
            "title": title,
            "company": company,
            "location": loc,
            "url": item.get("url", ""),
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "date_posted": safe_date(item.get("date")),
            "salary": salary,
            "summary": re.sub(r'<[^>]+>', '', (item.get("description", "")))[:500],
            "is_remote": True,
            "tags": item.get("tags", []),
            "dedup_key": normalize_dedup_key(company, title, loc),
        })

    return jobs[:kwargs.get("limit", 20)]


def search_arbeitnow(query: str, **kwargs) -> list:
    params = urllib.parse.urlencode({"page": 1})
    url = f"https://www.arbeitnow.com/api/job-board-api?{params}"

    data = api_get(url)
    if not data or "data" not in data:
        return []

    query_lower = query.lower()
    query_terms = query_lower.split()
    limit = kwargs.get("limit", 20)

    jobs = []
    for item in data["data"]:
        title = item.get("title", "")
        company = item.get("company_name", "Unknown")
        tags = [t.lower() for t in item.get("tags", [])]
        description = item.get("description", "").lower()

        searchable = f"{title} {company} {' '.join(tags)} {description}".lower()
        if not any(term in searchable for term in query_terms):
            continue

        loc = item.get("location", "Unknown")
        jobs.append({
            "id": f"arbeitnow_{item.get('slug', '')}",
            "source": "arbeitnow",
            "title": title,
            "company": company,
            "location": loc,
            "url": item.get("url", ""),
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "date_posted": safe_date(item.get("created_at")),
            "salary": "",
            "summary": re.sub(r'<[^>]+>', '', (item.get("description", "")))[:500],
            "is_remote": item.get("remote", False),
            "tags": item.get("tags", []),
            "dedup_key": normalize_dedup_key(company, title, loc),
        })

    return jobs[:limit]


def search_himalayas(query: str, **kwargs) -> list:
    params = urllib.parse.urlencode({"limit": 500})
    url = f"https://himalayas.app/jobs/api?{params}"

    data = api_get(url, headers={"User-Agent": "JobRecsBot/1.0"})
    if not data or "jobs" not in data:
        return []

    query_lower = query.lower()
    query_terms = query_lower.split()
    limit = kwargs.get("limit", 20)

    jobs = []
    for item in data["jobs"]:
        title = item.get("title", "")
        company = item.get("companyName", "Unknown")
        categories = [c.lower() for c in item.get("categories", [])]
        description = item.get("description", "").lower()

        searchable = f"{title} {company} {' '.join(categories)} {description}".lower()
        if not any(term in searchable for term in query_terms):
            continue

        loc_parts = []
        if item.get("locationRestrictions"):
            loc_parts = item["locationRestrictions"]
        loc = ", ".join(loc_parts) if loc_parts else "Remote"

        salary_min = item.get("minSalary")
        salary_max = item.get("maxSalary")
        salary = ""
        if salary_min and salary_max:
            salary = f"${salary_min:,}-${salary_max:,}"

        timezones = item.get("timezones", [])

        jobs.append({
            "id": f"himalayas_{item.get('id', '')}",
            "source": "himalayas",
            "title": title,
            "company": company,
            "location": loc,
            "url": item.get("applicationLink") or item.get("url", ""),
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "date_posted": safe_date(item.get("pubDate")),
            "salary": salary,
            "summary": re.sub(r'<[^>]+>', '', (item.get("description", "")))[:500],
            "is_remote": True,
            "timezones": timezones,
            "categories": item.get("categories", []),
            "dedup_key": normalize_dedup_key(company, title, loc),
        })

    return jobs[:limit]


def search_mycareersfuture(query: str, **kwargs) -> list:
    params = urllib.parse.urlencode({
        "search": query,
        "limit": min(kwargs.get("limit", 20), 100),
        "page": 0,
    })
    url = f"https://api.mycareersfuture.gov.sg/v2/jobs?{params}"
    headers = {"Content-Type": "application/json"}

    data = api_get(url, headers)
    if not data or "results" not in data:
        return []

    jobs = []
    for item in data["results"]:
        title = item.get("title", "Unknown")
        company = item.get("postedCompany", {}).get("name", "Unknown")
        loc = item.get("address", {}).get("formattedAddress", "Singapore")

        salary = ""
        sal = item.get("salary", {})
        if sal.get("minimum") and sal.get("maximum"):
            cur = sal.get("currency", "SGD")
            salary = f"{cur} {sal['minimum']:,}-{sal['maximum']:,}"

        job_url = f"https://www.mycareersfuture.gov.sg/job/{item.get('uuid', '')}"

        jobs.append({
            "id": f"mcf_{item.get('uuid', '')}",
            "source": "mycareersfuture",
            "title": title,
            "company": company,
            "location": loc,
            "url": job_url,
            "date_found": datetime.now().strftime("%Y-%m-%d"),
            "date_posted": safe_date(item.get("metadata", {}).get("newPostingDate")),
            "salary": salary,
            "summary": re.sub(r'<[^>]+>', '', (item.get("description", "")))[:500],
            "dedup_key": normalize_dedup_key(company, title, loc),
        })

    return jobs


# ---------------------------------------------------------------------------
# Registry and CLI
# ---------------------------------------------------------------------------

SOURCES = {
    "jsearch": search_jsearch,
    "adzuna": search_adzuna,
    "remoteok": search_remoteok,
    "arbeitnow": search_arbeitnow,
    "himalayas": search_himalayas,
    "mycareersfuture": search_mycareersfuture,
}


def main():
    parser = argparse.ArgumentParser(description="Search job APIs")
    parser.add_argument("--source", required=True, choices=list(SOURCES.keys()) + ["all"],
                        help="Which source to search (or 'all')")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--location", default="", help="Location filter")
    parser.add_argument("--country", default="us", help="Country code (ISO 3166)")
    parser.add_argument("--limit", type=int, default=20, help="Max results per source")
    args = parser.parse_args()

    load_env()

    sources_to_search = SOURCES.keys() if args.source == "all" else [args.source]
    all_jobs = []
    errors = []

    for source_name in sources_to_search:
        search_fn = SOURCES[source_name]
        try:
            results = search_fn(
                query=args.query,
                location=args.location,
                country=args.country,
                limit=args.limit,
            )
            all_jobs.extend(results)
        except Exception as e:
            errors.append({"source": source_name, "error": str(e)})
            print(json.dumps({"source": source_name, "error": str(e)}), file=sys.stderr)

    output = {
        "query": args.query,
        "location": args.location,
        "country": args.country,
        "timestamp": datetime.now().isoformat(),
        "sources_searched": list(sources_to_search),
        "total_results": len(all_jobs),
        "errors": errors,
        "jobs": all_jobs,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
