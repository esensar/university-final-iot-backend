from flask_restful import Resource, reqparse, abort, fields, marshal_with
import app.accounts as accounts


def user(user_dict):
    """
    Type definition of user object required as a parameter

    Required keys:
     * username - string
     * password - string

    :returns user dictionary with required keys
    :rtype dict
    :raises ValueError if parameter is not dict or is missing required keys
    """
    if not isinstance(user_dict, dict):
        raise ValueError("User should contain username, password and email")
    if ('username' not in user_dict or
            'password' not in user_dict):
        raise ValueError("User should contain username, password and email")
    return user_dict


class TokenResource(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('user', location='json', type=user,
                        help='User is not valid. Error: {error_msg}',
                        required=True)

    res_fields = {
            'status': fields.String(default='Success'),
            'token': fields.String
    }

    @marshal_with(res_fields)
    def post(self):
        try:
            args = TokenResource.parser.parse_args()['user']
            token = accounts.create_token(
                    args['username'],
                    args['password'])
            if token:
                return {'token': token}, 200
        except ValueError:
            abort(401, message='Invalid credentials', status='error')
