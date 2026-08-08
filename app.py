import datetime

from agents.job_agent import search_jobs
from Database.supabase_service import (
    get_profiles,
    job_exists,
    save_job
)
from agents.email_sender import send_email


MAX_DAILY_JOBS = 50


def daily_job_search():

    print("=" * 60)
    print("Running Daily Job Search")
    print(datetime.datetime.now())
    print("=" * 60)

    response = get_profiles()

    if not response.data:
        print("No profile found.")
        return

    profile = response.data[0]

    roles = [
        r.strip()
        for r in profile["roles"].split(",")
        if r.strip()
    ]

    experience = profile.get("experience") or 0

    total_jobs_checked = 0
    saved_jobs = 0

    email_jobs = []

    for role in roles:

        # Stop once 50 NEW jobs are saved
        if saved_jobs >= MAX_DAILY_JOBS:
            break

        print(f"\nSearching {role}...")

        try:
            jobs = search_jobs(
                role=role,
                experience=experience,
                results=20
            )

        except Exception as e:
            print(f"Error searching {role}: {e}")
            continue

        total_jobs_checked += len(jobs)

        print(f"Found {len(jobs)} jobs for {role}")

        for job in jobs:

            # Stop at 50 new jobs
            if saved_jobs >= MAX_DAILY_JOBS:
                break

            job_id = str(job.get("id", ""))

            if not job_id:
                continue

            # Skip jobs already stored in Supabase
            if job_exists(job_id):
                continue

            title = job.get("title", "")

            company = job.get(
                "company", {}
            ).get(
                "display_name", ""
            )

            location = job.get(
                "location", {}
            ).get(
                "display_name", ""
            )

            url = job.get(
                "redirect_url", ""
            )

            description = job.get(
                "description", ""
            )

            # Save new job
            save_job(
                job_id=job_id,
                title=title,
                company=company,
                location=location,
                url=url,
                role=role,
                score=0,
                description=description,
                source="Adzuna"
            )

            saved_jobs += 1

            # Add job to email
            email_jobs.append(
                {
                    "role": role,
                    "title": title,
                    "company": company,
                    "location": location,
                    "url": url
                }
            )

        print(f"{len(jobs)} jobs checked")

    # --------------------------------
    # SUMMARY
    # --------------------------------

    print("=" * 60)
    print(f"Jobs Checked : {total_jobs_checked}")
    print(f"New Jobs     : {saved_jobs}")
    print("=" * 60)

    # --------------------------------
    # SEND ONE DAILY EMAIL
    # --------------------------------

    if not email_jobs:

        print("No new jobs today.")
        return

    email_body = f"""
Hello Jaya,

Your AI Career Agent found {saved_jobs} NEW jobs today.

Jobs Checked: {total_jobs_checked}
New Jobs: {saved_jobs}

============================================================

"""

    for index, job in enumerate(email_jobs, start=1):

        email_body += f"""
{index}. {job['title']}

Role: {job['role']}
Company: {job['company']}
Location: {job['location']}
Apply: {job['url']}

------------------------------------------------------------
"""

    email_body += """

Open your Career Agent and start applying!

Good Luck 🚀
"""

    subject = f"🎯 {saved_jobs} New Jobs Found Today"

    try:

        send_email(
            subject=subject,
            body=email_body,
            receiver="mishra.jaya.1003@gmail.com"
        )

        print("✅ Daily reminder email sent successfully.")

    except Exception as e:

        print(f"❌ Email Error: {e}")


# --------------------------------
# RUN WHEN CALLED BY GITHUB ACTIONS
# --------------------------------

if __name__ == "__main__":
    daily_job_search()