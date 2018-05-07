from flask import Blueprint
from flask_restful import Api
from .resources.account import AccountResource
from .resources.token import TokenResource
from marshmallow import ValidationError

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Add resources
api.add_resource(AccountResource, '/v1/accounts')
api.add_resource(TokenResource, '/v1/token')


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
