from flask import Blueprint, jsonify
from database.db import get_db_connection

results_bp = Blueprint("results", __name__)

@results_bp.route("/results", methods=["GET"])
def get_results():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM results")
    rows = cursor.fetchall()
    conn.close()

    return jsonify({
        "count": len(rows),
        "results": [dict(row) for row in rows]
    })
