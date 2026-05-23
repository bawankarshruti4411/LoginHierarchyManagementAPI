from flask import Blueprint, jsonify
from db import get_db

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    db, cursor = get_db()
    cursor.execute(
        """
        SELECT *
        FROM company_users
        """
    )
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(users)


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    db, cursor = get_db()
    cursor.execute(
        """
        SELECT *
        FROM company_users
        WHERE id=%s
        """,
        (user_id,)
    )
    user = cursor.fetchone()
    cursor.close()
    db.close()
    return jsonify(user)
