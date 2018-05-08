from flask_restful import Resource, abort
from flask import g
from webargs import fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.accounts as accounts
from app.api import ProtectedResource, protected

user_args = {
    'user': fields.Nested({
        'username': fields.Str(required=True),
        'email': fields.Email(required=True),
        'password': fields.Str(required=True)
    }, required=True, location='json')
}


class AccountResource(ProtectedResource):

    @swag_from('swagger/get_account_spec.yaml')
    def get(self, account_id):
        if g.current_account.id == account_id:
            return g.current_account, 200
        abort(403, message='You can only get your own account', status='error')


class AccountListResource(Resource):
    @use_args(user_args)
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

    @protected
    def get(self):
        return '', 200
