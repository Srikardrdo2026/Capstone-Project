from flask import Blueprint, jsonify
from database.db import get_db_connection

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM results")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results WHERE prediction = 0")
    normal = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results WHERE prediction = 1")
    suspicious = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "total_predictions": total,
        "normal_users": normal,
        "suspicious_users": suspicious,
        "normal_percent": round((normal/total)*100, 2) if total else 0,
        "suspicious_percent": round((suspicious/total)*100, 2) if total else 0
    })
