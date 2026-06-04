from flask import Blueprint,jsonify,request
from middleware.auth_middleware import token_required
from middleware.role_middleware import role_required
from db import get_db


operations_bp = Blueprint(
"operations",
__name__
)




@operations_bp.route(
"/operations",
methods=["GET"]
)
@token_required
def get_operations(current_user):


    db,cursor=get_db()


    cursor.execute(
    """
    SELECT *
    FROM operations
    ORDER BY id DESC
    """
    )


    data=cursor.fetchall()


    cursor.close()

    db.close()


    return jsonify(data)







@operations_bp.route(
"/operations",
methods=["POST"]
)
@token_required
@role_required(["super_admin"])
def create_operation(current_user):


    try:


        data=request.json


        db,cursor=get_db()



        cursor.execute(
        """
        INSERT INTO operations
        (
        operation_name,
        description
        )

        VALUES(%s,%s)

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

        "message":
        "Operation Created"

        })


    except Exception as e:


        return jsonify({

        "error":str(e)

        }),500







@operations_bp.route(
"/operations/<int:id>",
methods=["DELETE"]
)
@token_required
@role_required(["super_admin"])
def delete_operation(
current_user,
id
):


    db,cursor=get_db()


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

    "message":
    "Deleted"

    })
