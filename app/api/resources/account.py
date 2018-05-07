from flask_restful import Resource, abort
from webargs import fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.accounts as accounts


class AccountResource(Resource):
    user_args = {
            'user': fields.Nested({
                'username': fields.Str(required=True),
                'email': fields.Email(required=True),
                'password': fields.Str(required=True)
            }, required=True, location='json')
    }

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

    @swag_from('swagger/get_account_spec.yaml')
    def get(self):
        return '', 200
