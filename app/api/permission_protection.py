from flask import g
from flask_restful import abort
from functools import wraps


def requires_permission(permission, action_name='Action'):
    def requires_permission_decorator(func):
        @wraps(func)
        def permission_protected_function(*args, **kwargs):
            if permission not in g.current_account.role.permissions:
                abort(403,
                      message=(action_name+' is not allowed'),
                      status='error')

            return func(*args, **kwargs)

        return permission_protected_function

    return requires_permission_decorator
