# 🤖 AI Career Agent

An AI-powered career automation system that helps job seekers discover relevant job opportunities, analyze job matches, track applications, and receive daily job reminders.

## 🚀 Features

- 📄 Resume-based profile extraction
- 🧠 Automatic skill extraction
- 💼 Target job role detection
- 🎯 Job matching based on skills and experience
- 🔎 Job search using Adzuna API
- 🏢 Company-wise job listings
- 📊 Job match scoring
- 📚 Missing skill identification
- 🔗 Direct job application links
- 💾 Supabase database integration
- 📧 Daily email job notifications
- ⏰ Automated job search scheduler
- 📌 Application preparation
- 📈 Career/job tracking

## 🛠️ Tech Stack

- Python
- Streamlit
- Supabase
- Adzuna Jobs API
- APScheduler
- Gmail SMTP
- Pandas
- PyPDF

## 📂 Project Structure

```text
career-agent/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── pages/
│   ├── Daily_Jobs.py
│   ├── Companies.py
│   ├── Recruiters.py
│   ├── Applications.py
│   ├── Resume.py
│   └── Analytics.py
│
├── agents/
│   ├── job_agent.py
│   ├── scheduler.py
│   └── email_sender.py
│
├── Database/
│   └── supabase_service.py
│
└── utils/
    ├── experience_extractor.py
    └── skill_extractor.py
