# Full Pipeline Run

Run the complete job search pipeline for today.

## Prerequisites
- `data/user_profile.md` must exist. If not, run the profile builder first by following the instructions in `.claude/commands/profile.md`.

## Pipeline Steps

Execute these steps in order:

### Step 1: Profile Check
- Read `data/user_profile.md` and confirm it exists and is current.
- If it doesn't exist, stop and tell the user to run `/project:profile` first.

### Step 2: Search
- Follow the procedure in `.claude/commands/search.md`.
- This searches all API sources and web sources, producing `data/runs/YYYY-MM-DD_raw.json`.

### Step 3: Present
- Follow the procedure in `.claude/commands/present.md`.
- This deduplicates, ranks, and presents the top jobs, producing `data/runs/YYYY-MM-DD.md`.

### Step 4: Feedback (interactive)
- Ask the user if they'd like to provide feedback now.
- If yes, follow the procedure in `.claude/commands/feedback.md`.
- If no, tell them they can run `/project:feedback` later.

## Scheduling

This pipeline is designed to be run daily. To set up a daily schedule:
- Use RemoteTrigger to create a scheduled run
- Or use CronCreate for session-only scheduling

## Notes
- If today's run already exists (`data/runs/YYYY-MM-DD_raw.json`), ask the user if they want to re-run or skip to presentation.
- Report timing and source counts at each step so the user knows what's happening.
