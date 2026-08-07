import re
from datetime import datetime


def extract_current_experience(resume_text):

    pattern = r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\s*[-–]\s*Present"

    match = re.search(pattern, resume_text, re.IGNORECASE)

    if not match:
        return 0

    date_text = match.group(0)

    date_text = (
        date_text.replace("Present", "")
        .replace("-", "")
        .replace("–", "")
        .strip()
    )

    try:
        start_date = datetime.strptime(date_text, "%B %Y")
    except ValueError:
        start_date = datetime.strptime(date_text, "%b %Y")

    today = datetime.today()

    months = (
        (today.year - start_date.year) * 12
        + today.month
        - start_date.month
    )

    return round(months / 12, 1)