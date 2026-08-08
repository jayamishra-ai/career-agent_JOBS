import streamlit as st

st.set_page_config(
    page_title="AI Career Agent",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Career Agent")

st.write("Welcome to your AI-powered Career Agent.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💼 Daily Jobs", "50")

with col2:
    st.metric("📅 Job Search", "Daily")

with col3:
    st.metric("📧 Reminder", "Email")

st.divider()

st.subheader("🚀 Career Agent")

st.write("""
Your Career Agent helps you find and apply for relevant opportunities.
""")

st.success("✅ Career Agent is running successfully!")

st.info("""
📧 **Daily Reminder**

Your GitHub Actions workflow searches for new jobs once a day
and sends the new-job list to your email.
""")