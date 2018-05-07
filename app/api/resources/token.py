from flask_restful import Resource, abort
from webargs import fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.accounts as accounts


class TokenResource(Resource):
    user_args = {
            'user': fields.Nested({
                'username': fields.Str(required=True),
                'password': fields.Str(required=True)
            }, required=True, location='json')
    }

    @use_args(user_args)
    @swag_from('swagger/create_token_spec.yaml')
    def post(self, args):
        try:
            args = args['user']
            token = accounts.create_token(
                    args['username'],
                    args['password'])
            if token:
                return {'status': 'success', 'token': token}, 200
        except ValueError:
            abort(401, message='Invalid credentials', status='error')
