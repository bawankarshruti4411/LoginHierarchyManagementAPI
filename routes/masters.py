from flask import Blueprint, jsonify
from db import get_db
from functools import lru_cache

masters_bp = Blueprint("masters", __name__)


@lru_cache(maxsize=1)
def fetch_masters():

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

    return tuple(
        tuple(item.items())
        for item in masters
    )


@masters_bp.route("/masters", methods=["GET"])
def get_masters():

    data = [
        dict(item)
        for item in fetch_masters()
    ]

    return jsonify(data)
