import streamlit as st
import urllib.parse

st.title("LinkedIn Recruiter Finder")

roles = [
    "Python Developer",
    ".NET Developer",
    "ML Engineer",
    "Generative AI Engineer"
]

selected_role = st.selectbox(
    "Select Role",
    roles
)

search_url = (
    "https://www.linkedin.com/search/results/people/?keywords="
    + urllib.parse.quote(selected_role + " recruiter")
)

st.link_button(
    "Find Recruiters",
    search_url
)


def generate_message(name, role):

    return f"""
Hi {name},

I am Jaya Mishra, an AI/ML Engineer and Software Developer with experience in Python, C#, .NET, Machine Learning, and Generative AI.

I came across your profile while exploring opportunities for {role} positions and would love to connect and learn about relevant opportunities.

Thank you for your time.

Best Regards,
Jaya Mishra
"""


recruiter = st.text_input("Recruiter Name")

if recruiter:

    st.text_area(
        "Connection Message",
        generate_message(
            recruiter,
            selected_role
        ),
        height=200
    )