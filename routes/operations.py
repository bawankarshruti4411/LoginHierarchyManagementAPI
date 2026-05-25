from flask import Blueprint, jsonify
from db import get_db
from functools import lru_cache

operations_bp = Blueprint("operations", __name__)


@lru_cache(maxsize=1)
def fetch_operations():

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

    return tuple(
        tuple(item.items())
        for item in operations
    )


@operations_bp.route("/operations", methods=["GET"])
def get_operations():

    data = [
        dict(item)
        for item in fetch_operations()
    ]

    return jsonify(data)
