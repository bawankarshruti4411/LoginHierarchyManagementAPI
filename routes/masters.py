from flask import Blueprint, jsonify, request

from db import get_db

masters_bp = Blueprint("masters", __name__)


@masters_bp.route("/masters", methods=["GET"])
def get_masters():

    db, cursor = get_db()

    cursor.execute(
        """
        SELECT *
        FROM masters
        ORDER BY id
        """
    )

    masters = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(masters)


@masters_bp.route("/masters", methods=["POST"])
def create_master():

    data = request.json

    db, cursor = get_db()

    cursor.execute(
        """
        INSERT INTO masters
        (name, description)
        VALUES (%s,%s)
        """,
        (
            data["name"],
            data["description"]
        )
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Master Created"
    })


@masters_bp.route("/masters/<int:id>", methods=["PUT"])
def update_master(id):

    data = request.json

    db, cursor = get_db()

    cursor.execute(
        """
        UPDATE masters
        SET name=%s,
            description=%s
        WHERE id=%s
        """,
        (
            data["name"],
            data["description"],
            id
        )
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Master Updated"
    })


@masters_bp.route("/masters/<int:id>", methods=["DELETE"])
def delete_master(id):

    db, cursor = get_db()

    cursor.execute(
        """
        DELETE FROM masters
        WHERE id=%s
        """,
        (id,)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({
        "message": "Master Deleted"
    })
