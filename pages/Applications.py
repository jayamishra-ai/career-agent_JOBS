import streamlit as st
from Database.supabase_service import get_profiles, save_application
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.title("Application Assistant")


def create_cover_letter_pdf(cover_letter):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("Cover Letter", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(
        Paragraph(
            cover_letter.replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer

response = get_profiles()

if not response.data:
    st.warning("No profile found")
    st.stop()

profile = response.data[0]

selected_job = st.session_state.get("selected_job")

if selected_job:

    st.subheader("Selected Job")

    st.write("Job Title:", selected_job["title"])
    st.write("Company:", selected_job["company"])
    st.write("Location:", selected_job["location"])

    st.link_button(
        "Open Application",
        selected_job["apply_url"]
    )

    cover_letter = f"""
    Dear Hiring Manager,

    I am writing to express my interest in the {selected_job['title']} position at {selected_job['company']}.

    With a 6-month Software Developer internship and professional experience as an Associate Software Developer, I have built a strong foundation in Python, C#, .NET, SQL Server, Machine Learning, Generative AI, Streamlit, and Supabase. Throughout my career, I have developed software solutions that improve efficiency, automate processes, and support data-driven decision making.

    In my current role, I contribute to the development and maintenance of enterprise applications, predictive analytics systems, and database-driven solutions. I have worked on projects involving large datasets, feature engineering, ranking algorithms, and real-time data processing. Additionally, I developed an AI Career Agent that automates resume analysis, skill extraction, job matching, recruiter outreach, and application tracking, significantly reducing manual effort and improving the job search workflow.

    I am particularly impressed by {selected_job['company']}'s commitment to innovation and technology-driven solutions. The opportunity to contribute my software development and AI expertise while continuing to learn and grow within a forward-thinking organization is especially exciting to me.

    My technical background, problem-solving abilities, and passion for building scalable applications enable me to contribute effectively to both engineering teams and business objectives. I am confident that my experience in software development, artificial intelligence, database technologies, and application design would allow me to make a meaningful contribution to your organization.

    Thank you for your time and consideration. I would welcome the opportunity to discuss how my skills, experience, and enthusiasm can contribute to the continued success of {selected_job['company']}.

    Sincerely,

    Jaya Mishra
    Associate Software Developer
    """

    st.subheader("Generated Cover Letter")

    st.text_area(
        "Cover Letter",
        cover_letter,
        height=300
    )
    pdf_file = create_cover_letter_pdf(cover_letter)

    st.download_button(
        label="📄 Download ATS Cover Letter PDF",
        data=pdf_file,
        file_name="Jaya_Mishra_Cover_Letter.pdf",
        mime="application/pdf"
    )

    if st.button("Save Application"):

        save_application(
            selected_job["company"],
            selected_job["title"]
        )

        st.success("Application Saved!")

else:
    st.info("Go to Job Finder and click Prepare Application.")