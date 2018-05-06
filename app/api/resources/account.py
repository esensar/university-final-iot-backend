from flask_restful import Resource, reqparse, abort
import app.accounts as accounts


def user(user_dict):
    """
    Type definition of user object required as a parameter

    Required keys:
     * username - string
     * password - string
     * email    - string

    :returns user dictionary with required keys
    :rtype dict
    :raises ValueError if parameter is not dict or is missing required keys
    """
    if not isinstance(user_dict, dict):
        raise ValueError("User should contain username, password and email")
    if ('username' not in user_dict or
            'password' not in user_dict or
            'email' not in user_dict):
        raise ValueError("User should contain username, password and email")
    return user_dict


class AccountResource(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('user', location='json', type=user,
                        help='User is not valid. Error: {error_msg}',
                        required=True)

    def post(self):
        try:
            args = AccountResource.parser.parse_args()['user']
            success = accounts.create_account(
                    args['username'],
                    args['email'],
                    args['password'])
            if success:
                return '', 201
        except ValueError:
            abort(422, message='Account already exists', status='error')
