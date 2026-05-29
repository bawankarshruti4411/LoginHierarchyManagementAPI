from flask import Blueprint, jsonify, request

from db import get_db

operations_bp = Blueprint("operations", __name__)


@operations_bp.route("/operations", methods=["GET"])
def get_operations():

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
def create_operation():

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
def update_operation(id):

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
def delete_operation(id):

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
