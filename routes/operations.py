from flask import Blueprint, jsonify
from db import get_db

operations_bp = Blueprint("operations", __name__)

@operations_bp.route("/operations", methods=["GET"])
def get_operations():
    db, cursor = get_db()
    cursor.execute(
        """
        SELECT *
        FROM operations
        """
    )
    operations = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(operations)
