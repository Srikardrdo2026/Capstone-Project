# Behavioral Fingerprinting for Cybersecurity

## Overview

This project implements a **backend system for behavioral fingerprinting** to identify and classify user behavior as **Normal** or **Suspicious** using machine learning. The system is designed for cybersecurity use cases such as IoT networks and distributed systems, where attackers may hide behind anonymity and encryption, but still leave identifiable behavioral patterns.

The project implements a complete **end-to-end system** consisting of:
- A machine learning–powered backend for prediction
- A static frontend for user interaction
- Offline model training
- Database-backed result storage

---

## Objectives

- Study and identify key behavioral patterns from user activity logs
- Design a machine learning model to classify behavior as normal or suspicious
- Build REST APIs to serve predictions
- Support real-time and batch (CSV) analysis
- Maintain clean separation between training, backend, and frontend

---

## Tech Stack

### Backend
- Python 3.11+
- Flask 3.0 (REST API)
- SQLite (persistent storage)
- Scikit-learn 1.3.2 (ML inference)
- Joblib (model loading)
- Pandas / NumPy (data handling)

**Backend Dependencies**
- Flask
- flask-cors
- pandas
- numpy
- scikit-learn
- joblib
- matplotlib
- requests


### Frontend
- HTML5
- CSS3
- JavaScript

### Tools
- Git & GitHub
- Postman (API testing)

## Project Structure

```text
Capstone-Project/
│
├── .git/                         # Git metadata (auto-generated)
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
│
Training/
|   |-- train_model.py            Model training script
|   |-- behavior_dataset.csv      Base dataset (1800 records)
|   |-- behavior_dataset_1M.csv   Large dataset (~1M records, excluded from Git)
|   |-- behavior_model.pkl        Trained ML model
|   |-- protocol_encoder.pkl      Saved protocol label encoder
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

## Setup Instructions (Local)

### 1. Clone Repository

```bash
git clone https://github.com/Srikardrdo2026/Capstone-Project.git
cd Capstone-Project
```

---

### 2. Backend Setup

```bash
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs at: `http://127.0.0.1:5000`

---

### 3. Frontend Setup

Open directly in browser:

```
Frontend/index.html
```

Or run a local server:

```bash
python -m http.server
```

---

---

## API Endpoints

| Method | Endpoint | Description |
|------|---------|------------|
| GET | /health | Health check |
| POST | /api/predict | Single behavior scan |
| POST | /api/predict-csv | CSV batch scan |
| GET | /api/analytics | Aggregated stats |
| GET | /api/results | Stored results |

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


## Notes

- Large generated datasets are excluded from GitHub
- Training is fully reproducible
- Backend uses pre-trained models only
- Clean separation of concerns maintained

---

## Conclusion

The project delivers a **production‑ready behavioral fingerprinting system** with ML inference, persistent storage, interactive visualization, and cloud deployment. It demonstrates practical application of machine learning in cybersecurity.
