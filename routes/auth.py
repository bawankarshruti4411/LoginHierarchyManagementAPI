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

    # Super Admin
    if (
        email == SUPER_ADMIN["email"]
        and password == SUPER_ADMIN["password"]
    ):
        return jsonify({"role": "super_admin"})

    db, cursor = get_db()

    # Company Admin
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
        cursor.close()
        db.close()
        return jsonify({
            "role": "company_admin",
            "admin_id": admin["id"]
        })

    # Company User
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
    cursor.close()
    db.close()

    if user:
        return jsonify({
            "role": "company_user",
            "user_id": user["id"]
        })

    return jsonify({"message": "Invalid Credentials"}), 401
