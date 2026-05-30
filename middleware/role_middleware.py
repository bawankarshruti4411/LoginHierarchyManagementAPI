from flask import jsonify
from functools import wraps

def role_required(roles):

    def decorator(func):

        @wraps(func)
        def wrapper(current_user, *args, **kwargs):

            if current_user["role"] not in roles:

                return jsonify({
                    "message": "Access Denied"
                }), 403

            return func(
                current_user,
                *args,
                **kwargs
            )

        return wrapper

    return decorator
