from flask import Blueprint, request, g
from flask_restful import Api, Resource, abort
from functools import wraps
from marshmallow import ValidationError
from app.accounts import validate_token


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


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
            abort(401, message='Unauthorized', status='error')

    return protected_function


class ProtectedResource(Resource):
    method_decorators = [protected]


def add_resources():
    from .resources.account import AccountResource
    from .resources.token import TokenResource

    api.add_resource(AccountResource, '/v1/accounts')
    api.add_resource(TokenResource, '/v1/token')


add_resources()


@api_bp.errorhandler(ValidationError)
@api_bp.errorhandler(422)
def handle_validation_error(e):
    return {'status': 'error', 'message': str(e)}, 422


@api_bp.errorhandler(Exception)
def handle_unknown_errors(e):
    return ({
        'status': 'failed',
        'message': 'Unknown error has occurred! ({0})'.format(str(e))
        }, 500)
