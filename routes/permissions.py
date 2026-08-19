from flask import Blueprint, jsonify, request
from db import get_db, release_db
from middleware.auth_middleware import token_required

permissions_bp = Blueprint("permissions", __name__)


@permissions_bp.route("/assign-operation", methods=["POST"])
@token_required
def assign_operation(current_user):

    data = request.json
    user_id = data["user_id"]
    operation_ids = data["operation_ids"]

    db, cursor = get_db()

    try:
        cursor.execute(
            """
            DELETE FROM user_operations
            WHERE user_id=%s
            """,
            (user_id,)
        )

        values = [
            (user_id, op_id)
            for op_id in operation_ids
        ]

        cursor.executemany(
            """
            INSERT INTO user_operations
            (user_id, operation_id)
            VALUES (%s,%s)
            """,
            values
        )

        db.commit()

        return jsonify({
            "message": "Permissions Assigned Successfully"
        })

    finally:
        cursor.close()
        release_db(db)


# NOTE: this route was previously missing the `user_id` parameter
# in the function signature even though the URL rule declares
# <int:user_id>. token_required passes current_user first, then
# Flask passes user_id as a keyword arg from the URL -- without
# it here, every call raised TypeError -> 500.
@permissions_bp.route("/user/<int:user_id>/operations", methods=["GET"])
@token_required
def get_user_operations(current_user, user_id):

    db, cursor = get_db()

    try:
        cursor.execute(
            """
            SELECT
                o.id,
                o.operation_name,
                o.description
            FROM operations o
            INNER JOIN user_operations uo
                ON o.id = uo.operation_id
            WHERE uo.user_id=%s
            """,
            (user_id,)
        )

        operations = cursor.fetchall()

        return jsonify(operations)

    finally:
        cursor.close()
        release_db(db)


@permissions_bp.route("/check-access", methods=["POST"])
@token_required
def check_access(current_user):

    data = request.json
    user_id = data["user_id"]
    operation_id = data["operation_id"]

    db, cursor = get_db()

    try:
        cursor.execute(
            """
            SELECT EXISTS(
                SELECT 1
                FROM user_operations
                WHERE user_id=%s
                AND operation_id=%s
            ) AS access
            """,
            (user_id, operation_id)
        )

        result = cursor.fetchone()

        return jsonify({
            "access": bool(result["access"])
        })

    finally:
        cursor.close()
        release_db(db)
