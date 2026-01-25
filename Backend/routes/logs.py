from flask import Blueprint, request, jsonify
from database.db import get_db_connection

logs_bp = Blueprint("logs", __name__)

@logs_bp.route("/logs", methods=["POST"])
def upload_logs():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No log data provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO raw_logs (log_data) VALUES (?)",
        (str(data),)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Log received successfully"
    }), 201
