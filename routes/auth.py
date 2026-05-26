import jwt

import datetime

from flask import current_app
from flask import Blueprint, request, jsonify
from db import get_db

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

    # Super Admin Check
    if (
        email == SUPER_ADMIN["email"]
        and password == SUPER_ADMIN["password"]
    ):
        token = jwt.encode(

    {
        "email": email,
        "role": "super_admin",
        "exp":
        datetime.datetime.utcnow()
        + datetime.timedelta(hours=24)
    },
    current_app.config["SECRET_KEY"],
    algorithm="HS256"
)
return jsonify({
    "role": "super_admin",
    "token": token
})
    db, cursor = get_db()

    cursor.execute(
        """
        SELECT id, 'company_admin' AS role
        FROM company_admins
        WHERE email=%s AND password=%s

        UNION ALL

        SELECT id, 'company_user' AS role
        FROM company_users
        WHERE email=%s AND password=%s

        LIMIT 1
        """,
        (email, password, email, password)
    )

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:

        return jsonify({
            "role": user["role"],
            "id": user["id"]
        })

    return jsonify({
        "message": "Invalid Credentials"
    }), 401
