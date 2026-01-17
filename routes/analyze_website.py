from flask import Blueprint, request, jsonify
import random
from services.preprocessing import extract_features
from services.predictor import predict_behavior
from database.db import get_db_connection

analyze_bp = Blueprint("analyze", __name__)

@analyze_bp.route("/analyze-website", methods=["POST"])
def analyze_website():
    data = request.get_json()
    website = data.get("website", "unknown")
    num_users = int(data.get("num_users", 100))

    normal = 0
    suspicious = 0

    conn = get_db_connection()
    cursor = conn.cursor()

    for _ in range(num_users):
        simulated_log = {
            "login_time": f"{random.randint(0,23)}:00",
            "session_duration": random.randint(1, 60),
            "commands": ["cmd"] * random.randint(5, 120),
            "failed_logins": random.randint(0, 5),
            "protocol": random.choice(["HTTPS", "SSH", "TOR"]),
            "typing_speed": random.randint(30, 140)
        }

        features = extract_features(simulated_log)
        result = predict_behavior(features)

        cursor.execute(
            "INSERT INTO results (prediction, confidence) VALUES (?, ?)",
            (result["prediction"], result["confidence"])
        )

        if result["prediction"] == 1:
            suspicious += 1
        else:
            normal += 1

    conn.commit()
    conn.close()

    total = normal + suspicious

    return jsonify({
        "website": website,
        "total_users": total,
        "normal_users": normal,
        "suspicious_users": suspicious,
        "normal_percent": round((normal/total)*100, 2),
        "suspicious_percent": round((suspicious/total)*100, 2),
        "note": "Results based on simulated behavioral patterns"
    })
