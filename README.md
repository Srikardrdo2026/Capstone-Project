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
- Support real-time, batch (CSV), and simulated website analysis.

---

## Tech Stack

### Backend

- **Python 3.11+**
- **Flask 3.0** (REST API)
- **SQLite** (local database)
- **Scikit-learn 1.3.2** (ML inference)
- **Joblib** (model loading)
- **Pandas / NumPy** (data handling)

### Testing & Tools

- Postman (API testing)
- Git & GitHub (version control)

---

## Project Structure

```text
backend/
│
├── app.py                  # Application entry point
├── config.py               # Configuration settings
├── requirements.txt
│
├── routes/
│   ├── health.py           # Health check endpoint
│   ├── logs.py             # Raw log ingestion
│   ├── predict.py          # Single prediction API
│   ├── predict_csv.py      # Batch CSV prediction API
│   ├── analyze_website.py  # Simulated website analysis
│   ├── analytics.py        # Prediction-based analytics
│   └── results.py          # Fetch stored predictions
│
├── services/
│   ├── preprocessing.py    # Behavioral feature extraction
│   └── predictor.py        # ML model + encoder inference
│
├── models/
│   ├── behavior_model.pkl  # Trained ML model
│   └── protocol_encoder.pkl# Saved protocol encoder
│
├── database/
│   └── db.py               # SQLite connection & schema
│
├── instance/
│   └── app.db              # SQLite database file
│
└── README.md
```

---

## API Endpoints

### Health

- `GET /health` – Check backend status

### Prediction

- `POST /api/predict` – Predict behavior for a single user log
- `POST /api/predict-csv` – Batch prediction from CSV file

### Website Analysis (Simulated)

- `POST /api/analyze-website`
  - Simulates multiple user sessions for a given website
  - Returns percentage of Normal vs Suspicious users

### Analytics

- `GET /api/analytics` – Aggregated prediction statistics
- `GET /api/results` – View stored prediction results

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
  - Website simulation
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

## Test 5: Website Analysis (Simulated)

### Request
- Method: `POST`
- URL: `/api/analyze-website`
- Headers: `Content-Type: application/json`

### Body
```json
{
  "website": "https://example.com",
  "num_users": 100
}
```

### Expected Response
```json
{
  "website": "https://example.com",
  "total_users": 100,
  "normal_users": 72,
  "suspicious_users": 28,
  "normal_percent": 72.0,
  "suspicious_percent": 28.0,
  "note": "Results based on simulated behavioral patterns"
}
```

### Purpose
- Demonstrates large-scale analysis
- Confirms simulation logic

---

## Test 6: Analytics Summary

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

## Test 7: Database Verification

### Request
- Method: `GET`
- URL: `/api/results`

### Expected Response
- List of stored prediction records
- Confirms persistence

---

## Conclusion

If all above tests pass:
- Backend APIs are functioning correctly
- ML integration is verified
- Database storage is validated
- System is ready for frontend integration

---

## Frontend Integration (Next Phase)

### Frontend Responsibilities

- Consume backend APIs only
- No ML logic on frontend
- No direct database access
- Visualization only

### Required API

- `POST /api/analyze-website`

Frontend should use the following response fields:

- `normal_percent`
- `suspicious_percent`

### Visualization

- Pie chart showing:
  - 🟢 Normal users (%)
  - 🔴 Suspicious users (%)
- Implemented using **Chart.js** with simple HTML & JavaScript

> Note: Backend already computes all statistics. Frontend must not perform calculations.

---

## Deployment (Optional)

For academic or low-traffic deployment:

- Deploy Flask backend on Render / Railway / AWS EC2
- Use SQLite (`app.db`) on the server

For production environments (future scope):

- Replace SQLite with PostgreSQL
- Add authentication and streaming log ingestion

---

## After Frontend Completion

- Integrate frontend with backend APIs
- Validate chart output against backend responses
- Capture screenshots for demo/report
- (Optional) Deploy backend if required

---

## Notes

- Feature extraction tables used during early development have been retired.
- Feature extraction is now an internal backend step.
- The system follows a clean separation of concerns between backend, ML, and frontend.

---

##
