from flask import Blueprint, jsonify
from db import get_db

masters_bp = Blueprint("masters", __name__)

@masters_bp.route("/masters", methods=["GET"])
def get_masters():
    db, cursor = get_db()
    cursor.execute(
        """
        SELECT *
        FROM masters
        """
    )
    masters = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(masters)
