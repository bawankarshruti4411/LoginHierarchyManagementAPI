from flask import Blueprint, jsonify, request
from db import get_db, release_db
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required

masters_bp = Blueprint("masters", __name__)


@masters_bp.route("/masters", methods=["GET"])
@token_required
@role_required(["super_admin"])
def get_masters(current_user):

    db, cursor = get_db()

    try:
        cursor.execute("""
            SELECT *
            FROM masters
            ORDER BY id
        """)

        masters = cursor.fetchall()

        return jsonify(masters)

    finally:
        cursor.close()
        release_db(db)


@masters_bp.route("/masters", methods=["POST"])
@token_required
@role_required(["super_admin"])
def create_master(current_user):

    data = request.json

    db, cursor = get_db()

    try:
        cursor.execute("""
            INSERT INTO masters
            (name, description)
            VALUES (%s, %s)
        """, (
            data["name"],
            data["description"]
        ))

        db.commit()

        return jsonify({
            "message": "Master Created"
        })

    finally:
        cursor.close()
        release_db(db)


@masters_bp.route("/masters/<int:id>", methods=["PUT"])
@token_required
@role_required(["super_admin"])
def update_master(current_user, id):

    data = request.json

    db, cursor = get_db()

    try:
        cursor.execute("""
            UPDATE masters
            SET name=%s,
                description=%s
            WHERE id=%s
        """, (
            data["name"],
            data["description"],
            id
        ))

        db.commit()

        return jsonify({
            "message": "Master Updated"
        })

    finally:
        cursor.close()
        release_db(db)


@masters_bp.route("/masters/<int:id>", methods=["DELETE"])
@token_required
@role_required(["super_admin"])
def delete_master(current_user, id):

    db, cursor = get_db()

    try:
        cursor.execute("""
            DELETE FROM masters
            WHERE id=%s
        """, (id,))

        db.commit()

        return jsonify({
            "message": "Master Deleted"
        })

    finally:
        cursor.close()
        release_db(db)
