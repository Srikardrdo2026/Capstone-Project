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

Postman collections and screenshots can be used as proof of correctness.

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
