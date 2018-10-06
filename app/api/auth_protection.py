import sys
from functools import wraps
from flask import request, g
from flask_restful import Resource, abort
from app.accounts.api import validate_token


def protected(func):
    @wraps(func)
    def protected_function(*args, **kwargs):
        try:
            token = request.headers['Authorization'] or None

            if not token:
                abort(401, message='Unauthorized', status='error')

            g.current_account = validate_token(token.replace("Bearer ", ""))
            if not g.current_account:
                abort(401, message='Unauthorized', status='error')
        except Exception:
            error_type, error_instance, traceback = sys.exc_info()
            print(str(error_type))
            print(str(error_instance))
            abort(401, message='Unauthorized', status='error')

        return func(*args, **kwargs)

    return protected_function


class ProtectedResource(Resource):
    method_decorators = [protected]
