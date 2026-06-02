from flask import Blueprint, jsonify, request

from db import get_db

from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required


users_bp = Blueprint("users", __name__)



# ============================
# GET ALL USERS
# ============================


@users_bp.route("/users", methods=["GET"])
@token_required
@role_required(["super_admin", "company_admin"])
def get_users(current_user):

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 20))

    offset = (page - 1) * limit


    db, cursor = get_db()


    cursor.execute(
        """
        SELECT COUNT(*) AS total
        FROM company_users
        """
    )


    total = cursor.fetchone()["total"]



    cursor.execute(
        """
        SELECT
            id,
            name,
            email

        FROM company_users

        ORDER BY id DESC

        LIMIT %s OFFSET %s
        """,
        (limit, offset)
    )



    users = cursor.fetchall()


    cursor.close()
    db.close()



    return jsonify({

        "total": total,

        "page": page,

        "limit": limit,

        "data": users

    })







# ============================
# CREATE USER
# ============================


@users_bp.route("/users", methods=["POST"])
@token_required
@role_required(["super_admin", "company_admin"])
def create_user(current_user):

    try:

        data = request.json


        name = data.get("name")
        email = data.get("email")
        password = data.get("password")


        if current_user["role"] == "company_admin":

            admin_id = current_user["id"]

        else:

            admin_id = data.get("admin_id", 1)



        db, cursor = get_db()


        cursor.execute(
            """
            INSERT INTO company_users
            (
                name,
                email,
                password,
                admin_id
            )

            VALUES(%s,%s,%s,%s)
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

        }), 201



    except Exception as e:


        print("CREATE USER ERROR:", e)


        return jsonify({

            "error": str(e)

        }), 500






# ============================
# DELETE USER
# ============================


@users_bp.route(
"/users/<int:user_id>",
methods=["DELETE"]
)
@token_required
@role_required(["super_admin", "company_admin"])
def delete_user(current_user,user_id):


    db,cursor = get_db()



    cursor.execute(

        """
        DELETE FROM user_operations

        WHERE user_id=%s

        """,

        (user_id,)

    )



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








# ============================
# UPDATE USER
# ============================


@users_bp.route(
"/users/<int:user_id>",
methods=["PUT"]
)
@token_required
@role_required(["super_admin", "company_admin"])
def update_user(current_user,user_id):


    data=request.json



    db,cursor=get_db()



    cursor.execute(

        """
        UPDATE company_users

        SET

        name=%s,

        email=%s,

        password=%s


        WHERE id=%s

        """,

        (
        data.get("name"),
        data.get("email"),
        data.get("password"),
        user_id
        )

    )



    db.commit()



    cursor.close()
    db.close()



    return jsonify({

        "message":
        "User Updated Successfully"

    })
