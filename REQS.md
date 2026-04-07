We are going to build a system aimed at finding jobs to apply for, based on preferences and qualifications. The system will be run every day to find new suggestions and it will support the following roles in trying to get from these input signals to a list of jobs. I am looking to first work with you to figure out what the best way of setting this up is - is it a combination of some custom skills, custom tools we can create from scratch, etc ? Let's first figure that out. The layout I thought about it a set of responsibilities that connect together. Take a look at the plan below and critique it (including decisions like using files to save state versus other types of storage like databases as well as the overall design components) We are then going to start working towards how to build this out:

1) Profile builder:
Responsibility: Loads the user’s resume and asks questions to form a clear user profile. These can include any unclear skills and capabilities of the user as well as what they are looking for in a role like location preferences, flexibilities, personal attributes like family situation, etc that can inform whether the user could move and how difficult it would be to do so. This is run only once in the very beginning in order to form the initial profile.
Inputs: User’s resume and any questions required to build a more complete profile other components can use.
Output: Builds and saves the user profile into user_profile.md
Bypassed if: A user profile already exists.

2) Domain Researcher:
Responsibility: Finds potential candidates for domains to use for sourcing jobs based on user profile. These can be job board sites (indeed, zip recruiter, etc.) as well as websites of interesting companies matching the user profile and preferences.
Inputs: user_profile.md
Outputs: A central repository of domains and URLs to check with explanations as to why each one was picked, saved in domains.md
Bypassed if: All of these conditions are correct - a) It has been less than 3 months since we last updated our domain list, b) the user profile has not changed significantly since the last domain update.

3) Crawler:
Responsibility: Searches for new jobs matching the user profile on the available domains. Updates the domain repository with any observed challenges or findings regarding each domain, so that the next time we crawl we can be more effective. Avoids jobs already seen if there is a record of such jobs.
Inputs: user_profile.md, domains.md, seen_jobs.json
Outputs: List of jobs matching the user preferences, found on the given domains, saved in new_jobs_raw.md

3) Verifier: Given the list of open job candidates, checks to make sure that they are not already visited and that they are still alive. May require different approaches for different sites. Writes learnings regarding the techniques used into domains.md so these can be leveraged next time. Cleared jobs are written into new_jobs_verified.md

4) Presenter: Takes the list of new, verified list of jobs and orders them based on relevance and probability of the user actually applying, based on prior interactions. Top 10 are presented to the user each day and these are appended to seen_jobs.json with the date and other information.
Inputs: user_profile.md, new_jobs_verified.md
Outputs: seen_jobs.json (append), top_5_jobs_[date].md

5) Profile tuner: Takes feedback from the user on the jobs - binary yes or no, as well as optionally reasons why. These are fed back into the user profile so that they can be used next time. The user may not provide feedback on all of the jobs.
Inputs:
Outputs: seen_jobs.json (modified with the feedback on each job), user_profile.md (modified to capture user preferences)