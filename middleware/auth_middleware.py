import jwt
from flask import request, jsonify
from functools import wraps
from flask import current_app
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # GET TOKEN FROM HEADER
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]

            if len(auth_header.split(" ")) > 1:
                token = auth_header.split(" ")[1]

        # TOKEN MISSING
        if not token:
            return jsonify({
                "message": "Token is missing"
            }), 401

        try:
            # VERIFY TOKEN
            data = jwt.decode(
                token,
                current_app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )

            current_user = data

        except Exception as e:
            return jsonify({
                "message": "Token is invalid",
                "error": str(e)
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated
