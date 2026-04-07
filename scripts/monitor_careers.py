#!/usr/bin/env python3
"""Monitor target company career pages for executive engineering roles.

Checks Greenhouse and Ashby JSON APIs for VP/Director/Head/CTO-level
engineering roles at target companies. Compares against previously seen
jobs to surface only new postings.

Usage:
    python3 scripts/monitor_careers.py [--all] [--company NAME]
    python3 scripts/monitor_careers.py --list-companies

Output: JSON with new executive engineering roles found.
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.request
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


# ---------------------------------------------------------------------------
# Company registry — ATS type and slug
# ---------------------------------------------------------------------------

COMPANIES = {
    "anthropic": {
        "name": "Anthropic",
        "ats": "greenhouse",
        "slug": "anthropic",
        "target": True,
    },
    "openai": {
        "name": "OpenAI",
        "ats": "ashby",
        "slug": "openai",
        "target": True,
    },
    "waymo": {
        "name": "Waymo",
        "ats": "greenhouse",
        "slug": "waymo",
        "target": True,
    },
    "stripe": {
        "name": "Stripe",
        "ats": "greenhouse",
        "slug": "stripe",
        "target": False,
    },
    "databricks": {
        "name": "Databricks",
        "ats": "greenhouse",
        "slug": "databricks",
        "target": False,
    },
    "scale_ai": {
        "name": "Scale AI",
        "ats": "greenhouse",
        "slug": "scaleai",
        "target": False,
    },
    "cloudflare": {
        "name": "Cloudflare",
        "ats": "greenhouse",
        "slug": "cloudflare",
        "target": False,
    },
    "figma": {
        "name": "Figma",
        "ats": "greenhouse",
        "slug": "figma",
        "target": False,
    },
    "datadog": {
        "name": "Datadog",
        "ats": "greenhouse",
        "slug": "datadog",
        "target": False,
    },
    "sony": {
        "name": "Sony Interactive Entertainment",
        "ats": "greenhouse",
        "slug": "sonyinteractiveentertainmentglobal",
        "target": True,
    },
}


# ---------------------------------------------------------------------------
# Title filters
# ---------------------------------------------------------------------------

EXEC_TITLE_PATTERNS = re.compile(
    r'\b(vp|vice\s+president|director|head\s+of|cto|chief\s+technology|'
    r'chief\s+ai|chief\s+engineering|svp|senior\s+vice\s+president|'
    r'gm\b|general\s+manager)',
    re.IGNORECASE
)

# Departments / title keywords that indicate engineering leadership
ENGINEERING_KEYWORDS = re.compile(
    r'(engineer|software|platform|infrastructure|ai|ml|machine\s+learning|'
    r'data|product\s+engineering|technical|technology|systems|cloud|'
    r'research|nlp|computer\s+vision|security\s+eng)',
    re.IGNORECASE
)

# Exclude these — not engineering leadership
EXCLUDE_PATTERNS = re.compile(
    r'(sales|marketing|finance|accounting|legal|counsel|litigation|'
    r'hr\b|human\s+resource|people\s+tech|'
    r'recruiting|talent\s+acquisition|communications|'
    r'content|editorial|policy|compliance|procurement|facilities|'
    r'customer\s+success|solutions\s+architect|field\s+cto|pre.?sales|'
    r'business\s+development|partnerships|partner\s+director|'
    r'account\s+director|channels?\b|campaign|'
    r'ad\s+operations|regulatory|data\s+center\s+delivery|'
    r'financial\s+systems|anaplan|industry\s+pursuit|'
    r'field\s+engineering|forward\s+deploy)',
    re.IGNORECASE
)


def api_get(url: str, headers: dict = None, timeout: int = 15):
    """Make a GET request and return parsed JSON."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as resp:
            return json.loads(resp.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        print(json.dumps({"error": str(e), "url": url}), file=sys.stderr)
        return None


def fetch_greenhouse(slug: str) -> list:
    """Fetch jobs from Greenhouse boards API."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    data = api_get(url)
    if not data or "jobs" not in data:
        return []

    jobs = []
    for item in data["jobs"]:
        title = item.get("title", "")
        loc_parts = [l.get("name", "") for l in item.get("offices", [])]
        location = ", ".join(loc_parts) if loc_parts else "Unknown"
        dept_parts = [d.get("name", "") for d in item.get("departments", [])]
        department = ", ".join(dept_parts) if dept_parts else ""

        jobs.append({
            "ats_id": str(item.get("id", "")),
            "title": title,
            "location": location,
            "department": department,
            "url": item.get("absolute_url", ""),
            "updated_at": (item.get("updated_at") or "")[:10],
        })
    return jobs


def fetch_ashby(slug: str) -> list:
    """Fetch jobs from Ashby posting API."""
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    data = api_get(url, headers)
    if not data or "jobs" not in data:
        return []

    jobs = []
    for item in data["jobs"]:
        title = item.get("title", "")
        location = item.get("location", "Unknown")
        department = item.get("departmentName", "") or item.get("department", "")
        employment_type = item.get("employmentType", "")

        jobs.append({
            "ats_id": item.get("id", ""),
            "title": title,
            "location": location,
            "department": department,
            "url": item.get("jobUrl", "") or item.get("applyUrl", ""),
            "updated_at": (item.get("publishedAt") or "")[:10],
        })
    return jobs


def is_exec_engineering_role(title: str, department: str) -> bool:
    """Check if a job title + department represents an executive engineering role."""
    combined = f"{title} {department}"

    # Must match an executive title pattern
    if not EXEC_TITLE_PATTERNS.search(title):
        return False

    # Must relate to engineering (in title or department)
    if not ENGINEERING_KEYWORDS.search(combined):
        return False

    # Must not be a non-engineering exec role
    if EXCLUDE_PATTERNS.search(combined):
        return False

    return True


def load_seen_ids(path: Path) -> set:
    """Load previously seen career monitor job IDs."""
    if path.exists():
        data = json.loads(path.read_text())
        return {j.get("ats_id") for j in data if j.get("ats_id")}
    return set()


def main():
    parser = argparse.ArgumentParser(description="Monitor target company career pages")
    parser.add_argument("--all", action="store_true", help="Check all companies")
    parser.add_argument("--company", help="Check a specific company by key")
    parser.add_argument("--list-companies", action="store_true", help="List available companies")
    parser.add_argument("--include-seen", action="store_true", help="Include previously seen jobs")
    args = parser.parse_args()

    if args.list_companies:
        for key, info in COMPANIES.items():
            marker = "★" if info["target"] else " "
            print(f"  {marker} {key:20s} {info['name']:35s} ({info['ats']})")
        return

    project_root = Path(__file__).resolve().parent.parent
    seen_path = project_root / "data" / "career_monitor_seen.json"
    seen_ids = load_seen_ids(seen_path) if not args.include_seen else set()

    companies_to_check = {}
    if args.company:
        if args.company in COMPANIES:
            companies_to_check = {args.company: COMPANIES[args.company]}
        else:
            print(f"Unknown company: {args.company}. Use --list-companies.", file=sys.stderr)
            sys.exit(1)
    else:
        companies_to_check = COMPANIES

    all_results = []
    for key, info in companies_to_check.items():
        if info["ats"] == "greenhouse":
            jobs = fetch_greenhouse(info["slug"])
        elif info["ats"] == "ashby":
            jobs = fetch_ashby(info["slug"])
        else:
            continue

        exec_jobs = [j for j in jobs if is_exec_engineering_role(j["title"], j["department"])]
        new_jobs = [j for j in exec_jobs if j["ats_id"] not in seen_ids]

        for j in new_jobs:
            j["company"] = info["name"]
            j["company_key"] = key
            j["is_target_company"] = info["target"]
            j["date_found"] = datetime.now().strftime("%Y-%m-%d")

        all_results.extend(new_jobs)

        total = len(jobs)
        exec_count = len(exec_jobs)
        new_count = len(new_jobs)
        print(f"{info['name']:35s} | {total:4d} total | {exec_count:3d} exec eng | {new_count:3d} new",
              file=sys.stderr)

    # Save all found exec IDs to seen file
    all_seen = list(seen_ids)
    for j in all_results:
        if j["ats_id"] not in seen_ids:
            all_seen.append(j["ats_id"])

    # Also save full records for reference
    existing_records = []
    if seen_path.exists():
        existing_records = json.loads(seen_path.read_text())
    existing_records.extend(all_results)
    seen_path.write_text(json.dumps(existing_records, indent=2))

    output = {
        "timestamp": datetime.now().isoformat(),
        "companies_checked": len(companies_to_check),
        "new_exec_engineering_roles": len(all_results),
        "jobs": all_results,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
