import datetime
from app.core import bcrypt
from .models import Account, Role
from .emailtoken import generate_confirmation_token, confirm_token


def create_account(username, email, password):
    """
    Tries to create account with given parameters. Raises error on failure

    :param username: Desired username for Account
    :param email: Desired email for Account
    :param password: Desired password for Account
    :type username: string
    :type email: string
    :type password: string
    :returns: Account and Email confirmation token if creation was successful
    :rtype: string
    :raises: ValueError if account already exists
    """
    if not Account.exists_with_any_of(username=username, email=email):
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        account = Account(username, pw_hash, email)
        account.save()

        emailtoken = generate_confirmation_token(account.email)
        return account, emailtoken

    raise ValueError("Account with given parameters already exists")


def confirm_email_token(token):
    try:
        email = confirm_token(token)
    except Exception:
        return False, None
    user = Account.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return True, user.email
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        user.save()
        return True, user.email


def update_account_role(account_id, role_id):
    """
    Tries to update account role

    :param account_id: Target account id
    :param role_id: New role role_id
    :type account_id: int
    :type role_id: int
    :returns: True if role is updated successfully
    :rtype: Boolean
    """
    acc = Account.get(id=account_id)
    acc.role_id = role_id
    acc.save()
    return acc


def create_role(display_name, permissions):
    """
    Tries to create role

    :param display_name: Name of role - display only
    :param permissions: List of strings - permissions that this role has
    :type display_name: String
    :type permissions: List of String
    :returns: True if role is successfully created
    :rtype: Boolean
    :raises: ValueError if role already exists
    """
    role = Role(display_name, permissions)
    role.save()
    return role


def get_role(role_id):
    """
    Tries to get role

    :param role_id: Id of role
    :type role_id: int
    :returns: Role if found
    :rtype: Role
    """
    return Role.get(role_id)


def get_all_roles():
    """
    Gets all roles

    :returns: Role list if found
    :rtype: List of Roles
    """
    return Role.get_all()


def create_token(username, password):
    """
    Tries to create token for account with given parameters.
    Raises error on failure

    :param username: username of Account
    :param password: password of Account
    :type username: string
    :type password: string
    :returns: created token
    :rtype: string
    :raises: ValueError if credentials are invalid or account does not exist
    """
    if not Account.exists(username=username):
        raise ValueError("Invalid credentials")

    account = Account.get(username=username)
    if not bcrypt.check_password_hash(account.password, password):
        raise ValueError("Invalid credentials")

    if not account.confirmed:
        raise ValueError("Email not confirmed")

    return account.create_auth_token()


def validate_token(token):
    """
    Validates token and returns associated account

    :param token: auth token to validate
    :type token: string
    :returns: created token
    :rtype: Account
    """
    return Account.validate_token(token)
