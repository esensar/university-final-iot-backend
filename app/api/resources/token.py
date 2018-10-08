from flask_restful import Resource, abort
from webargs import fields
from marshmallow import Schema
from webargs.flaskparser import use_args
from flasgger import swag_from
from app.api.auth_protection import ProtectedResource
import app.accounts.api as accounts


class UserInfoSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class TokenResource(Resource):

    @use_args(UserInfoSchema(), locations=('json',))
    @swag_from('swagger/create_token_spec.yaml')
    def post(self, args):
        try:
            token = accounts.create_token(
                    args['username'],
                    args['password'])
            if token:
                return {'status': 'success', 'token': token}, 200
        except ValueError:
            abort(401, message='Invalid credentials', status='error')


class ValidateTokenResource(ProtectedResource):
    @swag_from('swagger/validate_token_spec.yaml')
    def get(self):
        return {'status': 'success', 'message': 'Valid token'}, 200
