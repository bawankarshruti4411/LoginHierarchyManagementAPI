from flask import Blueprint, jsonify, request
from db import get_db

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users():

    page = int(
        request.args.get("page", 1)
    )

    limit = int(
        request.args.get("limit", 20)
    )

    offset = (page - 1) * limit

    db, cursor = get_db()

    cursor.execute(
        """
        SELECT id,
               name,
               email
        FROM company_users
        LIMIT %s OFFSET %s
        """,
        (limit, offset)
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
        SELECT id,
               name,
               email
        FROM company_users
        WHERE id=%s
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    return jsonify(user)
