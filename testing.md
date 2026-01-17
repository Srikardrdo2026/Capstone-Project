# Testing Guide – Backend API Validation

This document describes **how to test the backend APIs using Postman** and what outputs are expected. It serves as proof that the system works end-to-end.

---

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

Postman collections and screenshots can be attached as evidence during review or evaluation.

