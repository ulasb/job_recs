#!/bin/bash
# Daily job search pipeline — launched by launchd at 9am
# If the Mac was asleep, launchd runs this when it wakes up.

set -euo pipefail

PROJECT_DIR="/Users/ulas.bardak/git/job_recs"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

mkdir -p "$LOG_DIR"

echo "=== Daily job search started at $(date) ===" >> "$LOG_FILE"

cd "$PROJECT_DIR"

# Pull latest (in case feedback was pushed from another session)
git pull --rebase origin main >> "$LOG_FILE" 2>&1 || true

# Run Claude Code in print mode with the full pipeline
claude -p "Run the daily job search pipeline. Read and follow .claude/commands/search.md then .claude/commands/present.md.

IMPORTANT: This is a non-interactive run. Do NOT ask for feedback or wait for user input. Complete all steps and save results automatically.

Key reminders:
- Read data/user_profile.md FIRST, especially Learned Preferences
- Run python3 scripts/monitor_careers.py --all for career page monitoring
- Run python3 scripts/search.py --source jsearch for JSearch (API key in .env)
- Run python3 scripts/search.py --source adzuna for Adzuna (API key in .env)
- Use WebSearch for exec recruiter boards and target company career pages not covered by the monitor
- Use Indeed MCP for Indeed searches
- Apply ALL hard filters from Learned Preferences before presenting
- Deduplicate against data/seen_jobs.json
- Write the daily report to data/runs/$(date +%Y-%m-%d).md
- Update data/seen_jobs.json with new jobs found
- Commit and push all changes to GitHub
- Do NOT run the feedback step — the user will provide feedback separately
- Quality over quantity: 0-3 well-vetted roles is fine" >> "$LOG_FILE" 2>&1

echo "=== Daily job search completed at $(date) ===" >> "$LOG_FILE"
