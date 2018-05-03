from flask import Blueprint

accounts = Blueprint('accounts', __name__)


# Routes
@accounts.route("/")
def hello():
    return "Hello from accounts!"
