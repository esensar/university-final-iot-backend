import json
from app import db
from flask import request, current_app
from .models import Account, Role

def initialize_routes(accounts):
    @accounts.route("/", methods=['POST'])
    def create():
        json_body = json.loads(request.data)
        with current_app.app_context():
            acct = Account(2, json_body["user.username"],
                           json_body["user.password"])
            db.session.add(acct)
            db.session.commit()
            return "Success!"

