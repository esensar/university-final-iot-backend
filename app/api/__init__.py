from flask import Blueprint
from flask_restful import Api
from .resources.account import AccountResource
from .resources.token import TokenResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Add resources
api.add_resource(AccountResource, '/v1/accounts')
api.add_resource(TokenResource, '/v1/token')
