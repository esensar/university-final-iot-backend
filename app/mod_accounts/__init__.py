from flask import Blueprint
from .. import db

accounts = Blueprint('accounts', __name__)

# Models
from .models import Account
from .models import Role


# Routes
@accounts.route("/")
def hello():
    return "Hello from accounts!"
