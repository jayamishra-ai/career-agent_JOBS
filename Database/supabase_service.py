from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def save_profile(name, skills, roles, experience):

    return (
        supabase
        .table("profiles")
        .insert({
            "name": name,
            "skills": ",".join(skills),
            "roles": ",".join(roles),
            "experience": experience
        })
        .execute()
    )

def get_profiles():
    return (
        supabase
        .table("profiles")
        .select("*")
        .order("id", desc=True)
        .execute()
    )
def get_jobs():

    response = (
        supabase
        .table("jobs")
        .select("*")
        .execute()
    )

    return response.data
def save_application(company, role):

    return (
        supabase
        .table("applications")
        .insert({
            "company": company,
            "role": role,
            "status": "Applied"
        })
        .execute()
    )


def get_applications():

    return (
        supabase
        .table("applications")
        .select("*")
        .order("id", desc=True)
        .execute()
    )
def update_profile(name, skills, roles, experience):

    return (
        supabase
        .table("profiles")
        .update({
            "skills": ",".join(skills),
            "roles": ",".join(roles),
            "experience": experience
        })
        .eq("name", name)
        .execute()
    )
def save_job(job):

    return (
        supabase
        .table("jobs")
        .upsert({
            "title": job["title"],
            "company": job["company"]["display_name"],
            "location": job["location"]["display_name"],
            "apply_url": job["redirect_url"]
        })
        .execute()
    )
def save_job(job):

    return (
        supabase
        .table("jobs")
        .upsert({
            "job_id": str(job.get("id")),
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "url": job.get("redirect_url"),
            "description": job.get("description"),
            "role": job.get("role"),
            "source": "Adzuna",
            "match_score": job.get("match_score", 0)
        }, on_conflict="job_id")
        .execute()
    )
def job_exists(job_id):

    response = (
        supabase
        .table("jobs")
        .select("id")
        .eq("job_id", str(job_id))
        .execute()
    )

    return len(response.data) > 0


def save_job(
    job_id,
    title,
    company,
    location,
    url,
    role,
    score,
    description="",
    source="Adzuna"
):

    return (
        supabase
        .table("jobs")
        .insert({
            "job_id": str(job_id),
            "title": title,
            "company": company,
            "location": location,
            "url": url,
            "role": role,
            "match_score": score,
            "description": description,
            "source": source
        })
        .execute()
    )