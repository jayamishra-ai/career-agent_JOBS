import streamlit as st
import pandas as pd

from Database.supabase_service import get_profiles, get_jobs


st.set_page_config(
    page_title="Companies",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Companies Hiring Today")


# ==========================================
# Load Profile
# ==========================================

response = get_profiles()

if not response.data:
    st.warning("Please upload your resume first.")
    st.stop()

profile = response.data[0]


# ==========================================
# Get Saved Jobs From Supabase
# ==========================================

jobs = get_jobs()

if not jobs:
    st.warning("No jobs found in your database.")
    st.stop()


# ==========================================
# Convert Jobs To DataFrame
# ==========================================

data = []

for job in jobs:

    data.append({
        "company": job.get("company", ""),
        "title": job.get("title", ""),
        "location": job.get("location", ""),
        "url": job.get("url", ""),
        "role": job.get("role", ""),
        "match_score": job.get("match_score", 0),
        "created_at": job.get("created_at", "")
    })


df = pd.DataFrame(data)


# ==========================================
# Search Company
# ==========================================

search = st.text_input(
    "🔍 Search Company",
    placeholder="e.g. TCS, Infosys, Microsoft..."
)

if search:

    df = df[
        df["company"]
        .fillna("")
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


if df.empty:

    st.info("No companies found.")

    st.stop()


# ==========================================
# Company List
# ==========================================

companies = sorted(
    df["company"]
    .dropna()
    .unique()
)


st.success(
    f"🏢 {len(companies)} Companies Hiring"
)


# ==========================================
# Display Companies
# ==========================================

for company in companies:

    company_jobs = df[
        df["company"] == company
    ]

    with st.container(border=True):

        st.subheader(f"🏢 {company}")

        st.write(
            f"💼 **Open Positions:** "
            f"{len(company_jobs)}"
        )

        for index, row in company_jobs.iterrows():

            st.markdown(
                f"### {row['title']}"
            )

            st.write(
                f"📍 {row['location']}"
            )

            if row["role"]:

                st.caption(
                    f"Role: {row['role']}"
                )

            if row["match_score"]:

                st.progress(
                    min(
                        float(row["match_score"]) / 100,
                        1.0
                    )
                )

                st.write(
                    f"🎯 Match Score: "
                    f"{row['match_score']}%"
                )

            if row["url"]:

                st.link_button(
                    "Apply Now",
                    row["url"],
                    key=f"apply_{company}_{index}",
                    width="stretch"
                )

            st.divider()