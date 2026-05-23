from flask import Blueprint, jsonify, request
from db import get_db

permissions_bp = Blueprint("permissions", __name__)

@permissions_bp.route("/assign-operation", methods=["POST"])
def assign_operation():
    data = request.json
    user_id = data["user_id"]
    operation_ids = data["operation_ids"]

    db, cursor = get_db()

    # Remove old permissions
    cursor.execute(
        """
        DELETE FROM user_operations
        WHERE user_id=%s
        """,
        (user_id,)
    )

    # Insert new permissions
    for operation_id in operation_ids:
        cursor.execute(
            """
            INSERT INTO user_operations
            (user_id, operation_id)
            VALUES (%s,%s)
            """,
            (user_id, operation_id)
        )

    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "Permissions Assigned Successfully"})


@permissions_bp.route("/user/<int:user_id>/operations", methods=["GET"])
def get_user_operations(user_id):
    db, cursor = get_db()
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
    cursor.close()
    db.close()
    return jsonify(operations)


@permissions_bp.route("/check-access", methods=["POST"])
def check_access():
    data = request.json
    user_id = data["user_id"]
    operation_id = data["operation_id"]

    db, cursor = get_db()
    cursor.execute(
        """
        SELECT *
        FROM user_operations
        WHERE user_id=%s
        AND operation_id=%s
        """,
        (user_id, operation_id)
    )
    permission = cursor.fetchone()
    cursor.close()
    db.close()

    return jsonify({"access": bool(permission)})
