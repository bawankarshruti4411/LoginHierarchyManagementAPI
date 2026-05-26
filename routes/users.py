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


@users_bp.route("/users", methods=["POST"])
def create_user():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    admin_id = data.get("admin_id")



    db, cursor = get_db()



    cursor.execute(
        """
        INSERT INTO company_users
        (name, email, password, admin_id)

        VALUES (%s, %s, %s, %s)
        """,
        (
            name,
            email,
            password,
            admin_id
        )
    )



    db.commit()



    cursor.close()
    db.close()



    return jsonify({
        "message":
        "User Created Successfully"
    })

@users_bp.route(
    "/users/<int:user_id>",
    methods=["DELETE"]
)
def delete_user(user_id):

    try:

        db, cursor = get_db()



        # DELETE CHILD RECORDS FIRST

        cursor.execute(
            """
            DELETE FROM user_operations
            WHERE user_id=%s
            """,
            (user_id,)
        )



        # DELETE USER

        cursor.execute(
            """
            DELETE FROM company_users
            WHERE id=%s
            """,
            (user_id,)
        )



        db.commit()



        cursor.close()
        db.close()



        return jsonify({
            "message":
            "User Deleted Successfully"
        })



    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500
