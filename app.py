
import streamlit as st
from profile_agent import extract_resume_text
from utils.skill_extractor import extract_skills, get_target_roles
from Database.supabase_service import update_profile
from agents.scheduler import scheduler
from utils.experience_extractor import extract_current_experience
from agents.scheduler import scheduler

st.set_page_config(
    page_title="AI Career Agent",
    page_icon="🤖",
    layout="wide"
)

# ===========================
# Header
# ===========================
st.title("🤖 AI Career Agent")
st.markdown(
    """
Welcome to your **AI Career Assistant**.

This application helps you:

- 📄 Analyze your resume
- 🧠 Extract your technical skills
- 🎯 Recommend career roles
- 💼 Find matching jobs
- 👥 Discover recruiters
- 📊 Track applications
- 📈 Monitor your job search progress
"""
)

st.divider()

# ===========================
# Upload Resume
# ===========================
st.header("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose a PDF Resume",
    type=["pdf"]
)

if uploaded_file:

    with st.spinner("Analyzing Resume..."):

        text = extract_resume_text(uploaded_file)
        #experience = extract_current_experience(text)
        experience = 2
        st.success(f"Experience: {experience} Years")

        st.subheader("Experience")
        st.success(f"{experience} Years")
        skills = extract_skills(text)

        roles = get_target_roles(skills)

    st.success("✅ Resume analyzed successfully!")

    # Resume Preview
    with st.expander("📃 Resume Preview"):
        st.text_area(
            "Resume Content",
            text,
            height=250
        )

    # Skills
    st.subheader("🧠 Detected Skills")

    if skills:
        st.write(skills)
    else:
        st.warning("No skills detected.")

    # Roles
    st.subheader("🎯 Recommended Roles")

    if roles:
        st.write(roles)
    else:
        st.warning("No matching roles found.")

    st.divider()

    # Save Profile
    if st.button("💾 Save / Update Profile", use_container_width=True):

       
        update_profile("Jaya Mishra", skills, roles, experience)

        st.success("✅ Profile updated successfully!")

        st.balloons()

# ===========================
# Footer
# ===========================
st.divider()

st.info(
    """
### 🚀 Next Steps

1. Open **Dashboard** to view your career overview.
2. Visit **Daily Jobs** for personalized job recommendations.
3. Track your applications in **Applications**.
4. Explore recruiters and companies.
"""
)