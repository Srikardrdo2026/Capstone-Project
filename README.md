# Behavioral Fingerprinting for Cybersecurity

## Overview

This project implements a **backend system for behavioral fingerprinting** to identify and classify user behavior as **Normal** or **Suspicious** using machine learning. The system is designed for cybersecurity use cases such as IoT networks and distributed systems, where attackers may hide behind anonymity and encryption, but still leave identifiable behavioral patterns.

The backend is **fully implemented and tested**. The frontend visualization is intentionally decoupled and assigned as a separate task.

---

## Objectives

- Study and identify behavioral patterns from user activity or network logs.
- Extract behavioral fingerprints from raw logs.
- Classify users as *Normal* or *Suspicious* using a trained ML model.
- Store predictions and provide analytics via APIs.
- Support real-time, batch (CSV)

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

### Tools
- Git & GitHub
- Postman (API testing)
- Render (deployment)

---

## Project Structure

```text
Capstone-Project/
│
├── .git/                         # Git metadata (auto-generated)
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
│
├── Backend/                      # Backend (Flask + ML + Database)
│   │
│   ├── app.py                    # Flask application entry point
│   ├── config.py                 # Configuration settings
│   ├── requirements.txt          # Backend dependencies
│   │
│   ├── database/                 # Database handling
│   │   └── db.py                 # SQLite connection & schema
│   │
│   ├── instance/                 # Runtime-generated files
│   │   ├── .gitkeep              # Keeps folder in Git
│   │   └── app.db                # SQLite database (ignored in Git)
│   │
│   ├── models/                   # Trained ML artifacts
│   │   ├── behavior_model.pkl    # Trained ML classification model
│   │   └── protocol_encoder.pkl  # Saved protocol encoder
│   │
│   ├── routes/                   # REST API routes
│   │   ├── health.py             # Health check endpoint
│   │   ├── predict.py            # Single Scan prediction API
│   │   ├── predict_csv.py        # CSV batch prediction API
│   │   ├── analytics.py          # Aggregated analytics API
│   │   └── results.py            # Stored prediction results API
│   │
│   ├── services/                 # Core backend logic
│   │   ├── preprocessing.py      # Feature extraction logic
│   │   └── predictor.py          # ML model inference logic
│   │
│   ├── Tests/                    # Backend test scripts (optional)
│   ├── __pycache__/              # Python cache (ignored)
│   ├── venv/                     # Virtual environment (ignored)
│   └── .vscode/                  # Editor settings (ignored)
│
└── frontend/                     # Frontend (Static Web Application)
    │
    ├── index.html                # Single Scan UI
    ├── csv.html                  # CSV Batch Upload UI
    │
    ├── css/
    │   └── style.css             # Global frontend styles
    │
    └── js/
        ├── particles.js          # Background particle animation
        ├── predict.js            # Single Scan frontend logic
        └── csv.js                # CSV batch frontend logic

```

---

## API Endpoints

### Health

- `GET /health` – Check backend status

### Prediction

- `POST /api/predict` – Predict behavior for a single user log
- `POST /api/predict-csv` – Batch prediction from CSV file


### Analytics

- `GET /api/analytics` – Aggregated prediction statistics
- `GET /api/results` – View stored prediction results

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

---
## Database Design

### Results Table (Source of Truth)

```sql
results (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  prediction INTEGER,
  confidence REAL,
  created_at TIMESTAMP
)
```

All predictions (single, CSV, and simulated website users) are stored here.

---

## Testing

- All APIs are tested using **Postman**
- Test cases include:
  - Valid and invalid inputs
  - Single prediction
  - CSV batch prediction
  - Analytics verification

# Testing Guide – Backend API Validation

## Prerequisites

1. Python environment activated
2. Dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```
3. Backend server running:
   ```bash
   python app.py
   ```

Backend should start on:
```
http://127.0.0.1:5000
```

---

## Test 1: Health Check

### Request
- Method: `GET`
- URL: `/health`

### Expected Response
```json
{
  "status": "OK",
  "message": "Backend is running"
}
```

### Purpose
- Confirms backend server is active

---

## Test 2: Single User Prediction

### Request
- Method: `POST`
- URL: `/api/predict`
- Headers: `Content-Type: application/json`

### Body (JSON)
```json
{
  "login_time": "03:00",
  "session_duration": 5,
  "commands": ["ls", "sudo", "chmod"],
  "failed_logins": 4,
  "protocol": "TOR",
  "typing_speed": 120
}
```

### Expected Response
```json
{
  "prediction": "Suspicious",
  "confidence": 0.7
}
```

### Purpose
- Validates ML model inference
- Confirms prediction storage

---

## Test 3: Validation Check (Negative Test)

### Request
- Method: `POST`
- URL: `/api/predict`

### Body (Missing Field)
```json
{
  "login_time": "03:00",
  "session_duration": 5
}
```

### Expected Response
```json
{
  "error": "Invalid or missing input data"
}
```

### Purpose
- Confirms input validation is working

---

## Test 4: CSV Batch Prediction

### Prepare CSV File

`test.csv`
```csv
LoginHour,SessionDuration,CommandsCount,FailedLogins,Protocol,TypingSpeed
9,40,10,0,HTTPS,45
2,5,80,4,TOR,120
14,30,5,0,HTTPS,35
```

### Request
- Method: `POST`
- URL: `/api/predict-csv`
- Body type: `form-data`
- Key: `file`
- Value: upload `test.csv`

### Expected Response
```json
{
  "total_records": 3,
  "normal_users": 2,
  "suspicious_users": 1
}
```

### Purpose
- Validates batch processing
- Confirms multiple DB inserts

---


## Test 5: Analytics Summary

### Request
- Method: `GET`
- URL: `/api/analytics`

### Expected Response
```json
{
  "total_predictions": 104,
  "normal_users": 75,
  "suspicious_users": 29,
  "normal_percent": 72.1,
  "suspicious_percent": 27.9
}
```

### Purpose
- Confirms aggregated statistics
- Uses database as source of truth

---

## Test 6: Database Verification

### Request
- Method: `GET`
- URL: `/api/results`

### Expected Response
- List of stored prediction records
- Confirms persistence

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

