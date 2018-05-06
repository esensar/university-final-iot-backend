from app import bcrypt, status
from flask import request
from .models import Account


def initialize_routes(accounts):
    @accounts.route("", methods=['POST'])
    def create_account():
        print(request.data)
        user = request.data.get('user')
        if not Account.exists_with_any_of(
                username=user.get('username'), email=user.get('email')):
            password_hash = bcrypt.generate_password_hash(
                    user.get('password')
                    ).decode('utf-8')
            acct = Account(user.get('username'),
                           password_hash,
                           user.get('email'))
            acct.save()
            response = {
                'status': 'success',
                'message': 'Success!'
                }
            return response, status.HTTP_200_OK
        else:
            response = {
                'status': 'error',
                'message': 'User already exists!'
                }
            return response, status.HTTP_422_UNPROCESSABLE_ENTITY

    @accounts.route("/token", methods=['POST'])
    def create_token():
        print(request.data)
        user = request.data.get('user')
        if not user:
            response = {
                'status': 'error',
                'message': 'Invalid request'
                }
            return response, status.HTTP_400_BAD_REQUEST

        if not Account.exists(username=user.get('username')):
            response = {
                'status': 'error',
                'message': 'Invalid credentials'
                }
            return response, status.HTTP_401_UNAUTHORIZED

        account = Account.get(username=user.get('username'))
        if not bcrypt.check_password_hash(
                account.password, user.get('password')):
            response = {
                'status': 'error',
                'message': 'Invalid credentials'
                }
            return response, status.HTTP_401_UNAUTHORIZED

        response = {
                'status': 'success',
                'message': 'Successfully logged in',
                'token': account.create_auth_token()
            }
        return response, status.HTTP_200_OK
