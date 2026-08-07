SKILLS = [
    "Python",
    "C#",
    ".NET",
    "SQL",
    "SQL Server",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "Generative AI",
    "LLM",
    "RAG",
    "Agentic AI",
    "Pandas",
    "NumPy",
    "Scikit-Learn",
    "MySQL",
    "Git",
    "Streamlit",
    "Supabase"
]

def extract_skills(text):

    found_skills = []

    text = text.lower()

    for skill in SKILLS:
        if skill.lower() in text:
            found_skills.append(skill)

    return list(set(found_skills))


def get_target_roles(skills):

    roles = []

    if "Python" in skills:
        roles.append("Python Developer")

    if "C#" in skills or ".NET" in skills:
        roles.append(".NET Developer")

    if "Machine Learning" in skills:
        roles.append("ML Engineer")

    if "Generative AI" in skills:
        roles.append("Generative AI Engineer")

    return roles