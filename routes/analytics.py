from flask import Blueprint, jsonify
from database.db import get_db_connection

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics", methods=["GET"])
def get_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Total records
    cursor.execute("SELECT COUNT(*) FROM features")
    total_records = cursor.fetchone()[0]

    # Average session duration
    cursor.execute("SELECT AVG(session_duration) FROM features")
    avg_session_duration = cursor.fetchone()[0] or 0

    # Privileged command usage count
    cursor.execute("""
        SELECT COUNT(*) FROM features
        WHERE uses_privileged_cmd = 1
    """)
    privileged_count = cursor.fetchone()[0]

    # Login hour distribution
    cursor.execute("""
        SELECT login_hour, COUNT(*) as count
        FROM features
        GROUP BY login_hour
        ORDER BY login_hour
    """)
    login_distribution = [
        {"hour": row["login_hour"], "count": row["count"]}
        for row in cursor.fetchall()
    ]

    # Protocol distribution
    cursor.execute("""
        SELECT protocol_encoded, COUNT(*) as count
        FROM features
        GROUP BY protocol_encoded
    """)
    protocol_distribution = [
        {"protocol": row["protocol_encoded"], "count": row["count"]}
        for row in cursor.fetchall()
    ]

    conn.close()

    return jsonify({
        "total_records": total_records,
        "average_session_duration": round(avg_session_duration, 2),
        "privileged_command_usage": privileged_count,
        "login_hour_distribution": login_distribution,
        "protocol_distribution": protocol_distribution
    })
