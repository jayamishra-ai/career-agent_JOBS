import streamlit as st
from Database.supabase_service import (
    get_profiles,
    get_jobs,
    get_applications
)

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 AI Career Agent Dashboard")
st.caption("Your daily job search overview")

# -----------------------------
# Load Data
# -----------------------------
try:
    profiles = get_profiles().data
except:
    profiles = []

try:
    jobs = get_jobs()
except:
    jobs = []

try:
    applications = get_applications().data
except:
    applications = []

# -----------------------------
# Profile Information
# -----------------------------
if profiles:
    profile = profiles[0]

    name = profile.get("name", "User")
    skills = profile.get("skills", "")
    roles = profile.get("roles", "")

else:
    name = "User"
    skills = ""
    roles = ""

# -----------------------------
# Dashboard Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👤 Profile",
        name
    )

with col2:
    st.metric(
        "💼 Jobs Found",
        len(jobs)
    )

with col3:
    st.metric(
        "📤 Applications",
        len(applications)
    )

with col4:
    st.metric(
        "🎯 Target Roles",
        len(roles.split(",")) if roles else 0
    )

st.divider()

# -----------------------------
# Skills
# -----------------------------
left, right = st.columns([2,1])

with left:

    st.subheader("🧠 Skills")

    if skills:

        for skill in skills.split(","):
            st.badge(skill.strip())

    else:
        st.info("No skills available.")

with right:

    st.subheader("🎯 Roles")

    if roles:

        for role in roles.split(","):
            st.write("✅", role.strip())

    else:
        st.info("No roles available.")

st.divider()

# -----------------------------
# Recent Applications
# -----------------------------
st.subheader("📋 Recent Applications")

if applications:

    st.dataframe(
        applications,
        use_container_width=True
    )

else:

    st.info("No applications yet.")

st.divider()

# -----------------------------
# Latest Jobs
# -----------------------------
st.subheader("🔥 Latest Jobs")

if jobs:

    for job in jobs[:5]:

        with st.container(border=True):

            st.subheader(job.get("title",""))

            st.write("🏢", job.get("company",""))

            st.write("📍", job.get("location",""))

            if job.get("apply_url"):
                st.link_button(
                    "Apply",
                    job["apply_url"]
                )

else:

    st.info("No jobs found.")

st.divider()

st.success("🚀 Welcome back! Start by checking today's recommended jobs.")