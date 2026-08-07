import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search"


def search_jobs(
    role,
    experience=0,
    location="India",
    results=20,
    remote=False,
    page=1
):

    if not APP_ID or not APP_KEY:
        print("❌ Missing Adzuna credentials")
        return []

    query = role

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": query,
        "where": location,
        "results_per_page": results,
        "sort_by": "date",
        "content-type": "application/json"
    }

    if remote:
        params["what"] += " remote"

    url = f"{BASE_URL}/{page}"

    for attempt in range(3):

        try:

            response = requests.get(
                url,
                params=params,
                timeout=20
            )

            # Adzuna temporarily unavailable
            if response.status_code == 503:

                print(
                    f"⚠️ Adzuna 503 for {role} | "
                    f"{location} | Attempt {attempt + 1}/3"
                )

                time.sleep(5)
                continue

            response.raise_for_status()

            jobs = response.json().get("results", [])

            print(
                f"Found {len(jobs)} jobs for "
                f"{role} | {location}"
            )

            return jobs

        except requests.RequestException as e:

            print(
                f"❌ Adzuna error: "
                f"{role} | {location} | {e}"
            )

            if attempt < 2:
                time.sleep(5)

    return []