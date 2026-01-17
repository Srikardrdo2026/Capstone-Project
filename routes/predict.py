from flask import Blueprint, request, jsonify
from services.preprocessing import extract_features
from services.predictor import predict_behavior
from database.db import get_db_connection

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    log_data = request.get_json()

    # -------- BASIC VALIDATION --------
    if not log_data:
        return jsonify({"error": "No log data provided"}), 400

    required_fields = [
        "login_time",
        "session_duration",
        "commands",
        "failed_logins",
        "protocol",
        "typing_speed"
    ]

    for field in required_fields:
        if field not in log_data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Validate login_time format (HH:MM)
    if ":" not in log_data["login_time"]:
        return jsonify({"error": "Invalid login_time format. Expected HH:MM"}), 400

    # Validate numeric fields
    try:
        int(log_data["session_duration"])
        int(log_data["failed_logins"])
        float(log_data["typing_speed"])
    except ValueError:
        return jsonify({"error": "Invalid numeric value in input"}), 400

    # Validate commands
    if not isinstance(log_data["commands"], list):
        return jsonify({"error": "Commands must be a list"}), 400
    # ---------------------------------

    # Step 1: Extract behavioral features
    features = extract_features(log_data)

    # Step 2: Predict using ML model
    result = predict_behavior(features)

    # Step 3: Store result in database
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO results (prediction, confidence)
        VALUES (?, ?)
    """, (result["prediction"], result["confidence"]))

    conn.commit()
    conn.close()

    # Step 4: Return response
    return jsonify({
        "features": features,
        "prediction": "Suspicious" if result["prediction"] == 1 else "Normal",
        "confidence": result["confidence"]
    }), 200
