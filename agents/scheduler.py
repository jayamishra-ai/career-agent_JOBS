from apscheduler.schedulers.background import BackgroundScheduler
from agents.job_agent import search_jobs
from Database.supabase_service import (
    get_profiles,
    job_exists,
    save_job
)
from agents.email_sender import send_email
import datetime

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
    ]

    experience = profile.get("experience", 0)

    total_jobs = 0
    new_jobs = 0
    saved_jobs = 0

    email_body = ""

    for role in roles:

        # Stop after 50 saved jobs
        if saved_jobs >= MAX_DAILY_JOBS:
            break

        print(f"\nSearching {role}...")

        jobs = search_jobs(
            role=role,
            experience=experience,
            results=20      # Fetch only 20 per role
        )

        total_jobs += len(jobs)

        for job in jobs:

            if saved_jobs >= MAX_DAILY_JOBS:
                break

            job_id = str(job.get("id"))

            if job_exists(job_id):
                continue

            title = job.get("title", "")
            company = job.get("company", {}).get("display_name", "")
            location = job.get("location", {}).get("display_name", "")
            url = job.get("redirect_url", "")
            description = job.get("description", "")

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
            new_jobs += 1

            email_body += (
                f"Role: {role}\n"
                f"Job: {title}\n"
                f"Company: {company}\n"
                f"Location: {location}\n"
                f"Apply: {url}\n"
                + "-" * 60 + "\n"
            )

        print(f"{len(jobs)} jobs checked")

    print("=" * 60)
    print(f"Jobs Checked : {total_jobs}")
    print(f"New Jobs     : {new_jobs}")
    print(f"Saved Today  : {saved_jobs}")
    print("=" * 60)

    if new_jobs == 0:
        print("No new jobs today.")
        return

    subject = f"🎯 {new_jobs} New Jobs Found Today"

    body = f"""
Hello Jaya,

Your AI Career Agent found {new_jobs} NEW jobs today.

Jobs Checked : {total_jobs}
Jobs Saved   : {saved_jobs}

==============================

{email_body}

==============================

Open your Career Agent and start applying!

Good Luck 🚀
"""

    send_email(
        subject=subject,
        body=body,
        receiver="mishra.jaya.1003@gmail.com"   # Replace with your actual email
    )

    print("✅ Email sent successfully.")


if __name__ == "__main__":
    daily_job_search()