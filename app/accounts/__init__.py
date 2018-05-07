from app import bcrypt
from flask import Blueprint
from .models import Account

accounts_bp = Blueprint('accounts', __name__)


def create_account(username, email, password):
    """
    Tries to create account with given parameters. Raises error on failure

    :param username: Desired username for Account
    :param email: Desired email for Account
    :param password: Desired password for Account
    :type username: string
    :type email: string
    :type password: string
    :returns True if account is successfully created
    :rtype Boolean
    :raises ValueError if account already exists
    """
    if not Account.exists_with_any_of(username=username, email=email):
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        account = Account(username, pw_hash, email)
        account.save()
        return True

    raise ValueError("Account with given parameters already exists")


def create_token(username, password):
    """
    Tries to create token for account with given parameters.
    Raises error on failure

    :param username: username of Account
    :param password: password of Account
    :type username: string
    :type password: string
    :returns created token
    :rtype string
    :raises ValueError if credentials are invalid or account does not exist
    """
    if not Account.exists(username=username):
        raise ValueError("Invalid credentials")

    account = Account.get(username=username)
    if not bcrypt.check_password_hash(account.password, password):
        raise ValueError("Invalid credentials")

    return account.create_auth_token()


def validate_token(token):
    """
    Validates token and returns associated account

    :param token: auth token to validate
    :type token: string
    :returns created token
    :rtype Account
    """
    return Account.validate_token(token)
