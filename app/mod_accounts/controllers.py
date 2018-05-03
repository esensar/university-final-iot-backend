from app import db
from flask import request, jsonify, abort
from .models import Account, Role

def initialize_routes(accounts):
    @accounts.route("/", methods=['POST'])
    def create():
        print(request.data)
        user = request.data.get('user')
        acct = Account(user.get('username'),
                       user.get('password'),
                       user.get('email'),
                       2)
        acct.save()
        response = jsonify({
            'message':'Success!'
            })
        response.status_code = 200
        return response

