from flask_restful import Resource, abort
from flask import g
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.accounts as accounts
from app.api import ProtectedResource


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserWrapperSchema(Schema):
    user = fields.Nested(UserSchema, required=True, location='json')


class AccountResource(ProtectedResource):
    @swag_from('swagger/get_account_spec.yaml')
    def get(self, account_id):
        if g.current_account.id == account_id:
            return UserWrapperSchema().dump({'user': g.current_account}), 200
        abort(403, message='You can only get your own account', status='error')


class AccountListResource(Resource):
    @use_args(UserWrapperSchema())
    @swag_from('swagger/create_account_spec.yaml')
    def post(self, args):
        try:
            args = args['user']
            success = accounts.create_account(
                    args['username'],
                    args['email'],
                    args['password'])
            if success:
                return '', 201
        except ValueError:
            abort(422, message='Account already exists', status='error')
