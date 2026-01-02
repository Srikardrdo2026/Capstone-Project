Behavioral Fingerprinting for Cybersecurity
Backend System (Phase 1–3)


Project Overview
----------------
In modern cyber threat landscapes, attackers often hide their identity using anonymity tools and encryption.
While identities may be concealed, behavioral patterns such as access timing, command usage, protocol preferences,
and session characteristics can act as digital fingerprints.

This project focuses on building a backend system that:
• Ingests real-world-like user activity and network logs
• Extracts meaningful behavioral features
• Provides analytical insights
• Prepares the data pipeline for machine-learning–based classification

This document describes the backend implementation up to Phase 3.

Project Objectives
------------------
1. Identify key behavioral patterns from logs that act as digital fingerprints.
2. Design a machine-learning–ready framework (ML integration planned in Phase 4).

Backend Scope (Current Status)
-----------------------------
Implemented (Phase 1–3):
• Flask backend setup and routing
• SQLite database integration
• JSON log ingestion
• Behavioral feature extraction
• Feature storage
• Analytics APIs
• Fully testable backend without ML dependency

Planned (Phase 4):
• ML model integration
• Prediction APIs
• CSV upload support
• Input validation

Technology Stack
----------------
Backend: Python 3.11+, Flask 3.0
Data Processing: Pandas, NumPy
Machine Learning (Planned): Scikit-learn, Joblib
Database: SQLite
Visualization: Matplotlib
Tools: VS Code, Git, Postman

Database Schema
---------------
Tables:
raw_logs, features, results (Phase 4)

Project Structure
-----------------
backend/
│
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── requirements.txt
│
├── routes/
│   ├── health.py           # Health check endpoint
│   ├── logs.py             # Raw log ingestion
│   ├── features.py         # Feature extraction API
│   ├── analytics.py        # Behavioral analytics API
│   └── results.py          # Prediction results (Phase 4)
│
├── services/
│   └── preprocessing.py    # Behavioral feature extraction logic
│
├── database/
│   └── db.py               # SQLite connection & schema
│
├── instance/
│   └── app.db              # SQLite database file
│
└── README.md

How to Run
---------
Virtual Environment Setup (Recommended)

It is recommended to use a virtual environment to manage project dependencies.

1️⃣ Create a virtual environment
python -m venv venv

2️⃣ Activate the virtual environment

Windows - venv\Scripts\activate
Linux / macOS - source venv/bin/activate

3️⃣ Install required packages
pip install -r requirements.txt

🚀 Run the Backend
4️⃣ Start the application
python app.py

5️⃣ Access the backend
http://127.0.0.1:5000

Verification of Available API Endpoints (Phase 1–3). 
---------------------------------------------------

-> Health Check - GET /health

Response

{
  "status": "OK",
  "message": "Backend is running"
}

-> Upload Raw Logs - POST /api/logs

Sample Body

{
  "user": "anonymous",
  "protocol": "SSH",
  "login_time": "23:40",
  "commands": ["ls", "cd", "sudo"],
  "session_duration": 120
}

-> Extract Behavioral Features - POST /api/extract-features

Response

{
  "message": "Behavioral features extracted successfully",
  "features": {
    "login_hour": 23,
    "command_count": 3,
    "uses_privileged_cmd": 1,
    "session_duration": 120,
    "protocol_encoded": 1
  }
}

-> Analytics & Insights - GET /api/analytics

Response

{
  "total_records": 10,
  "average_session_duration": 95.4,
  "privileged_command_usage": 3,
  "login_hour_distribution": [...],
  "protocol_distribution": [...]
}

Database Verification
---------------------
To verify the database is working:

import sqlite3
conn = sqlite3.connect("instance/app.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

Expected tables: raw_logs, features, results

Future Enhancements
-------------------
• ML-based classification
• CSV ingestion
• Prediction confidence
• Dashboard integration

