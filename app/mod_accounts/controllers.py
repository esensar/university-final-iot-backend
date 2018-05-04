from app import bcrypt
from flask import request, jsonify
from .models import Account


def initialize_routes(accounts):
    @accounts.route("/", methods=['POST'])
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
            response = jsonify({
                'status': 'success',
                'message': 'Success!'
                })
            response.status_code = 200
            return response
        else:
            response = jsonify({
                'status': 'error',
                'message': 'User already exists!'
                })
            response.status_code = 422
            return response

    @accounts.route("/token", methods=['POST'])
    def create_token():
        print(request.data)
        user = request.data.get('user')
        if not user:
            response = jsonify({
                'status': 'error',
                'message': 'Invalid request'
                })
            response.status_code = 400
            return response

        if not Account.exists(username=user.get('username')):
            response = jsonify({
                'status': 'error',
                'message': 'Invalid credentials'
                })
            response.status_code = 422
            return response

        account = Account.get(username=user.get('username'))
        if not bcrypt.check_password_hash(
                account.password, user.get('password')):
            response = jsonify({
                'status': 'error',
                'message': 'Invalid credentials'
                })
            response.status_code = 422
            return response

        response = jsonify({
                'status': 'success',
                'message': 'Successfully logged in',
                'token': account.create_auth_token()
            })
        response.status_code = 200
        return response
