from flask import Blueprint, request, jsonify
from db import get_db
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint("auth", __name__)

SUPER_ADMIN = {
    "email": "superadmin@gmail.com",
    "password": "admin123"
}


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    # SUPER ADMIN LOGIN
    if (
        email == SUPER_ADMIN["email"]
        and password == SUPER_ADMIN["password"]
    ):

        token = jwt.encode(
            {
                "email": email,
                "role": "super_admin",
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(hours=24)
            },

            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        return jsonify({
            "role": "super_admin",
            "token": token
        })

    # DATABASE CONNECTION
    db, cursor = get_db()

    # COMPANY ADMIN LOGIN
    cursor.execute(
        """
        SELECT *
        FROM company_admins
        WHERE email=%s
        AND password=%s
        """,

        (email, password)
    )

    admin = cursor.fetchone()

    if admin:

        token = jwt.encode(
            {
                "admin_id": admin["id"],
                "email": admin["email"],
                "role": "company_admin",
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(hours=24)
            },

            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        cursor.close()
        db.close()

        return jsonify({
            "role": "company_admin",
            "admin_id": admin["id"],
            "token": token
        })

    # COMPANY USER LOGIN
    cursor.execute(
        """
        SELECT *
        FROM company_users
        WHERE email=%s
        AND password=%s
        """,

        (email, password)
    )

    user = cursor.fetchone()

    if user:

        token = jwt.encode(
            {
                "user_id": user["id"],
                "email": user["email"],
                "role": "company_user",
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(hours=24)
            },

            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        cursor.close()
        db.close()

        return jsonify({
            "role": "company_user",
            "user_id": user["id"],
            "token": token
        })

    cursor.close()
    db.close()

    return jsonify({
        "message": "Invalid Credentials"
    }), 401
