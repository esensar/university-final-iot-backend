from app import db
from flask import request, current_app
from .models import Account, Role

def initialize_routes(accounts):
    @accounts.route("/", methods=['POST'])
    def create():
        with current_app.app_context():
            print(request.data)
            user = request.data.get('user')
            acct = Account(user.get('username'),
                           user.get('password'),
                           user.get('email'),
                           2)
            acct.save()
            return "Success!"

