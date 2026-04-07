# Profile Builder

Build or update the user's job search profile.

## If `data/user_profile.md` does not exist (first run):

1. Try to load the user's resume using the Indeed `get_resume` MCP tool. If that fails, ask the user to paste or describe their resume.

2. Parse the resume to extract: job titles, skills, experience level, industries, education, locations worked.

3. Ask the user the following questions interactively (adapt based on what the resume already answers):

   **Job preferences:**
   - What job titles are you targeting?
   - What industries interest you?
   - Preferred company size (startup, mid, enterprise, no preference)?
   - Full-time, contract, or both?
   - What's your target compensation range?

   **Location & mobility:**
   - Where are you currently located?
   - Are you open to remote work? Hybrid? On-site?
   - Which countries/cities would you consider relocating to?
   - Any constraints on relocation (family, visa, etc.)?
   - Timezone preferences for remote work?

   **Priorities & dealbreakers:**
   - What matters most to you in a role (growth, compensation, mission, tech stack, culture)?
   - Any dealbreakers (e.g., no travel, must have visa sponsorship, no startups)?
   - Languages you can work in?

4. Write `data/user_profile.md` with all gathered information in a clear, structured format.

## If `data/user_profile.md` already exists (update mode):

1. Read the existing profile and show the user a summary.
2. Ask what they'd like to update.
3. Make the requested changes while preserving the rest.

## Profile format

```markdown
# User Profile

Last updated: YYYY-MM-DD

## Professional Summary
[2-3 sentence summary]

## Skills & Experience
- **Experience level**: [Junior/Mid/Senior/Lead/Executive]
- **Years of experience**: N
- **Key skills**: [list]
- **Industries**: [list]
- **Education**: [summary]

## Job Preferences
- **Target titles**: [list]
- **Job types**: [Full-time/Contract/Both]
- **Company size**: [preference]
- **Target compensation**: [range with currency]
- **Must-haves**: [list]

## Location Preferences
- **Current location**: [city, country]
- **Remote**: [Yes/No/Hybrid]
- **Open to relocation**: [Yes/No]
- **Target locations**: [list of countries/cities]
- **Relocation constraints**: [any constraints]
- **Timezone preferences**: [range or specific]
- **Work languages**: [list]

## Priorities
[Ordered list of what matters most]

## Dealbreakers
[List of non-negotiables]

## Learned Preferences
_Updated automatically from job feedback._

[Initially empty — populated as the user provides feedback on presented jobs]
```
