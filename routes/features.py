from flask import Blueprint, request, jsonify
from services.preprocessing import extract_features
from database.db import get_db_connection

features_bp = Blueprint("features", __name__)

@features_bp.route("/extract-features", methods=["POST"])
def extract_behavioral_features():
    log_data = request.get_json()

    if not log_data:
        return jsonify({"error": "No log data provided"}), 400

    features = extract_features(log_data)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO features (
            login_hour,
            command_count,
            uses_privileged_cmd,
            session_duration,
            protocol_encoded
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        features["login_hour"],
        features["command_count"],
        features["uses_privileged_cmd"],
        features["session_duration"],
        features["protocol_encoded"]
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Behavioral features extracted successfully",
        "features": features
    }), 201
