from flask import Blueprint, request, jsonify
import pandas as pd
from services.preprocessing import extract_features
from services.predictor import predict_behavior
from database.db import get_db_connection

predict_csv_bp = Blueprint("predict_csv", __name__)

@predict_csv_bp.route("/predict-csv", methods=["POST"])
def predict_csv():
    if "file" not in request.files:
        return jsonify({"error": "CSV file missing"}), 400

    file = request.files["file"]
    df = pd.read_csv(file)

    normal = 0
    suspicious = 0

    conn = get_db_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        log_data = {
            "login_time": row["LoginHour"],
            "session_duration": row["SessionDuration"],
            "commands": ["cmd"] * int(row["CommandsCount"]),
            "failed_logins": row["FailedLogins"],
            "protocol": row["Protocol"],
            "typing_speed": row["TypingSpeed"]
        }

        features = extract_features(log_data)
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
        "total_records": total,
        "normal_users": normal,
        "suspicious_users": suspicious
    })
