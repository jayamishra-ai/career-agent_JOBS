import streamlit as st
from Database.supabase_service import get_profiles
from agents.job_agent import search_jobs

st.set_page_config(
    page_title="Daily Jobs",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Daily Job Recommendations")


def calculate_match(job, skills):

    score = 0

    text = (
        job.get("title", "") + " " +
        job.get("description", "")
    ).lower()

    for skill in skills:
        if skill.strip().lower() in text:
            score += 10

    return min(score, 100)


def find_missing_skills(job, user_skills):

    common_skills = [
        "Python",
        "SQL",
        "AWS",
        "Docker",
        "Machine Learning",
        "C#",
        ".NET",
        "Java",
        "Azure",
        "LLM",
        "Generative AI"
    ]

    text = (
        job.get("title", "") + " " +
        job.get("description", "")
    ).lower()

    detected = []

    for skill in common_skills:
        if skill.lower() in text:
            detected.append(skill)

    missing = []

    for skill in detected:
        if skill.lower() not in [
            s.strip().lower()
            for s in user_skills
        ]:
            missing.append(skill)

    return detected, missing


# -------------------------
# Load Profile
# -------------------------

response = get_profiles()

if not response.data:
    st.warning("Please upload your resume first.")
    st.stop()

profile = response.data[0]

roles = [
    r.strip()
    for r in profile["roles"].split(",")
]

skills = [
    s.strip()
    for s in profile["skills"].split(",")
]

experience = profile.get("experience") or 0

st.info(f"💼 Experience: {experience} Years")

minimum_match = st.slider(
    "Minimum Match Score",
    0,
    100,
    30
)

# -------------------------
# Search Jobs
# -------------------------

for role in roles:

    st.header(f"💼 {role}")

    jobs = search_jobs(
        role=role,
        experience=experience
    )

    if not jobs:
        st.warning(f"No jobs found for {role}")
        continue

    scored_jobs = []

    seen = set()

    for job in jobs:

        job_id = job.get("id")

        if job_id in seen:
            continue

        seen.add(job_id)

        score = calculate_match(job, skills)

        if score >= minimum_match:
            scored_jobs.append((score, job))

    scored_jobs.sort(
        key=lambda x: x[0],
        reverse=True
    )

    st.success(f"Found {len(scored_jobs)} matching jobs")

    for index, (match_score, job) in enumerate(scored_jobs):

        title = job.get("title", "N/A")
        company = job.get("company", {}).get(
            "display_name",
            "N/A"
        )
        location = job.get("location", {}).get(
            "display_name",
            "N/A"
        )

        description = job.get("description", "")

        apply_url = job.get("redirect_url")

        created = job.get("created", "N/A")

        detected_skills, missing_skills = find_missing_skills(
            job,
            skills
        )

        with st.container(border=True):

            st.subheader(title)

            st.write(f"🏢 **Company:** {company}")
            st.write(f"📍 **Location:** {location}")
            st.write(f"📅 **Posted:** {created}")

            st.progress(match_score / 100)

            st.success(f"🎯 Match Score: {match_score}%")

            if detected_skills:
                st.write(
                    "✅ Required Skills:",
                    ", ".join(detected_skills)
                )

            if missing_skills:
                st.warning(
                    "📚 Missing Skills: "
                    + ", ".join(missing_skills)
                )
            else:
                st.success("Perfect Skill Match!")

            with st.expander("Job Description"):
                st.write(description)

            col1, col2 = st.columns(2)

            with col1:

             if st.button(
                    "Prepare Application",
                    key=f"prepare_{role}_{job.get('id')}_{index}"
             ):

                    st.session_state.selected_job = {
                        "title": title,
                        "company": company,
                        "location": location,
                        "apply_url": apply_url
                    }

                    st.success(
                        "Application Prepared!"
                    )

            with col2:

                if apply_url:
                    st.link_button(
                    "Apply Now",
                    apply_url,
                    width="stretch"
                )

    st.divider()