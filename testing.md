# Behavioral Fingerprinting for Cybersecurity

## Overview
This project implements a **full‑stack behavioral fingerprinting system** to classify user behavior as **Normal** or **Suspicious** using machine learning. It targets cybersecurity scenarios (IoT and distributed systems) where attackers hide identities but still expose **behavioral patterns**.

The system is **fully deployed** with a live backend and a static frontend, connected via REST APIs.

---

## Objectives
- Identify behavioral patterns from user activity or network logs
- Generate behavioral fingerprints from session data
- Classify users as *Normal* or *Suspicious*
- Persist predictions and provide analytics
- Support **single scan**, **CSV batch**, and **website‑level simulation**

---

## Live Deployment
- **Frontend:** https://behavioral-fingerprinting-frontend.onrender.com
- **Backend:** https://behavioral-fingerprinting-backend.onrender.com

---

## Tech Stack

### Backend
- Python 3.11+
- Flask 3.0 (REST API)
- SQLite (persistent storage)
- Scikit‑learn 1.3.2 (ML inference)
- Joblib (model loading)
- Pandas / NumPy (data handling)

### Frontend
- HTML5, CSS3, JavaScript
- Chart.js (visualization)

### Tools
- Git & GitHub
- Postman (API testing)
- Render (deployment)

---

## Project Structure

```text
backend/
│
├── app.py                  # Flask app entry
├── config.py               # Configuration
├── requirements.txt
│
├── routes/
│   ├── health.py           # Health check
│   ├── predict.py          # Single scan API
│   ├── predict_csv.py      # CSV batch API
│   ├── analyze_website.py  # Website simulation API
│   ├── analytics.py        # Aggregated stats
│   └── results.py          # Stored predictions
│
├── services/
│   ├── preprocessing.py    # Feature extraction
│   └── predictor.py        # ML inference
│
├── models/
│   ├── behavior_model.pkl
│   └── protocol_encoder.pkl
│
├── database/
│   └── db.py               # SQLite schema & connection
│
├── instance/
│   └── app.db              # Runtime DB (ignored in Git)
│
└── README.md
```

---

## API Endpoints

### Health
- `GET /health`

### Prediction
- `POST /api/predict` – Single user scan
- `POST /api/predict-csv` – Batch CSV scan

### Website Simulation
- `POST /api/analyze-website`

### Analytics
- `GET /api/analytics`
- `GET /api/results`

---

## Single Scan – Input Specification (Frontend)

The **Single Scan** feature collects session‑level behavioral attributes and submits them to the backend for classification.

### Input Fields

| Field | Type | Range / Options | Description | Example |
|-----|-----|----------------|-------------|---------|
| Login Hour | Number | 0–23 | Hour of login | 14 |
| Session Duration | Number | ≥ 0 | Session length (minutes) | 45 |
| Number of Commands | Number | ≥ 0 | Commands executed | 20 |
| Failed Login Attempts | Number | ≥ 0 | Failed attempts | 1 |
| Protocol Used | Select | HTTPS, SSH, FTP, TOR | Network protocol | SSH |
| Typing Speed | Number | ≥ 0 | Words per minute | 55 |

### Derived API Payload
```json
{
  "login_time": "14:00",
  "session_duration": 45,
  "commands": ["cmd", "cmd", "cmd"],
  "failed_logins": 1,
  "protocol": "SSH",
  "typing_speed": 55
}
```

### Frontend Validation Rules
- Login hour must be between 0–23
- Numeric fields must be non‑negative
- All fields are mandatory

---

## Database Design

### Table: `results`
```sql
results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  prediction TEXT,
  confidence REAL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

All predictions (single, CSV, website simulation) are stored here.

---

## Testing

### Backend Testing
- Health check
- Single scan inference
- CSV batch processing
- Website simulation
- Analytics aggregation

### Frontend Testing
- Page load & navigation
- Input validation
- Single scan UI
- Website analysis pie chart (hover tooltips)
- CSV upload handling

All tests passed successfully.

---

## Deployment

### Backend
- Deployed on Render as a Web Service
- Flask bound to dynamic port
- SQLite DB created at runtime

### Frontend
- Deployed on Render as a Static Site
- Consumes backend APIs over HTTPS

---

## Conclusion

The project delivers a **production‑ready behavioral fingerprinting system** with ML inference, persistent storage, interactive visualization, and cloud deployment. It demonstrates practical application of machine learning in cybersecurity.

