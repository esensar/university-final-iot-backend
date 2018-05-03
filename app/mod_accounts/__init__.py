from flask import Blueprint
from .controllers import initialize_routes

accounts = Blueprint('accounts', __name__)

initialize_routes(accounts)
