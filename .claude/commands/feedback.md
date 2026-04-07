# Feedback Collector

Collect user feedback on presented jobs and update the profile.

## Prerequisites
- A daily report must exist at `data/runs/YYYY-MM-DD.md`. If not, tell the user to run `/project:present` first.
- `data/seen_jobs.json` and `data/user_profile.md` must exist.

## Procedure

1. **Load the latest daily report**: Find the most recent `data/runs/YYYY-MM-DD.md` file and read it.

2. **Ask for feedback**: Present each job from the report and ask:
   - "Would you apply for this? (yes/no/skip)"
   - If no: "Brief reason why not?" (optional — user can skip)
   - If yes: "What specifically appeals to you?" (optional)

   The user can respond to all at once (e.g., "1: yes, 2: no - too junior, 3: skip, 4: yes - great company") or one by one.

3. **Update seen_jobs.json**: For each job the user provided feedback on, find it in `data/seen_jobs.json` by its `id` and update:
   - `feedback`: "yes", "no", or null (if skipped)
   - `feedback_reason`: the reason given, or null

4. **Analyze patterns**: After collecting feedback, look for patterns:
   - Are there recurring reasons for rejection? (e.g., "too senior", "wrong industry", "no visa sponsorship")
   - Are there common traits in accepted jobs? (e.g., always says yes to remote, prefers certain company sizes)
   - Does the feedback reveal preferences not captured in the profile?

5. **Update user_profile.md**: Add or update the "Learned Preferences" section based on the patterns found. Examples:
   - "Consistently rejects jobs requiring 10+ years experience — may want mid-level roles"
   - "Always interested in companies with < 100 employees — strong startup preference"
   - "Rejects all non-remote positions despite profile saying 'hybrid ok' — update to remote-only"

   Be conservative — only add a preference after seeing it 2+ times. Note the date and evidence.

6. **Report**: Summarize what was learned and what profile updates were made.

## Notes
- The user may not provide feedback on all jobs — that's fine, leave those as `feedback: null`.
- Don't push for reasons if the user doesn't want to elaborate — a simple yes/no is valuable.
- Over time, the learned preferences become the most important part of the profile, as they capture real behavior rather than stated preferences.
