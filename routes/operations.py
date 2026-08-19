from flask import Blueprint, jsonify, request
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from db import get_db, release_db


operations_bp = Blueprint("operations", __name__)


@operations_bp.route("/operations", methods=["GET"])
@token_required
def get_operations(current_user):

    db, cursor = get_db()

    try:
        cursor.execute(
            """
            SELECT *
            FROM operations
            ORDER BY id DESC
            """
        )

        data = cursor.fetchall()

        return jsonify(data)

    finally:
        cursor.close()
        release_db(db)


@operations_bp.route("/operations", methods=["POST"])
@token_required
@role_required(["super_admin", "company_admin"])
def create_operation(current_user):

    db = None
    cursor = None

    try:
        data = request.json

        db, cursor = get_db()

        cursor.execute(
            """
            INSERT INTO operations
            (operation_name, description)
            VALUES(%s,%s)
            """,
            (
                data["operation_name"],
                data["description"]
            )
        )

        db.commit()

        return jsonify({
            "message": "Operation Created"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            release_db(db)


@operations_bp.route("/operations/<int:id>", methods=["DELETE"])
@token_required
@role_required(["super_admin", "company_admin"])
def delete_operation(current_user, id):

    db = None
    cursor = None

    try:
        db, cursor = get_db()

        cursor.execute(
            """
            DELETE FROM operations
            WHERE id=%s
            """,
            (id,)
        )

        db.commit()

        return jsonify({
            "message": "Operation Deleted Successfully"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if db:
            release_db(db)
