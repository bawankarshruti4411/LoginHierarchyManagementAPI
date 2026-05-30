from flask import Blueprint, jsonify, request
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from db import get_db
operations_bp = Blueprint("operations", __name__)
@operations_bp.route("/operations", methods=["GET"])
@token_required
def get_operations(current_user):
    db, cursor = get_db()
    cursor.execute(
        """
        SELECT *
        FROM operations
        ORDER BY id
        """
    )
    operations = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(operations)
@operations_bp.route("/operations", methods=["POST"])
@token_required
@role_required(["super_admin"])
def create_operation(current_user):
    data = request.json
    db, cursor = get_db()
    cursor.execute(
        """
        INSERT INTO operations
        (operation_name, description)
        VALUES (%s,%s)
        """,
        (
            data["operation_name"],
            data["description"]
        )
    )
    db.commit()
    cursor.close()
    db.close()

    return jsonify({
        "message": "Operation Created"
    })
@operations_bp.route("/operations/<int:id>", methods=["PUT"])
@token_required
@role_required(["super_admin"])
def update_operation(current_user,user_id):
    data = request.json
    db, cursor = get_db()
    cursor.execute(
        """
        UPDATE operations
        SET operation_name=%s,
            description=%s
        WHERE id=%s
        """,
        (
            data["operation_name"],
            data["description"],
            id
        )
    )

    db.commit()
    cursor.close()
    db.close()
    return jsonify({
        "message": "Operation Updated"
    })
@operations_bp.route("/operations/<int:id>", methods=["DELETE"])
@token_required
@role_required(["super_admin"])
def delete_operation(current_user,user_id):
    db, cursor = get_db()
    cursor.execute(
        """
        DELETE FROM operations
        WHERE id=%s
        """,
        (id,)
    )
    db.commit()
    cursor.close()
    db.close()
    return jsonify({
        "message": "Operation Deleted"
    })
