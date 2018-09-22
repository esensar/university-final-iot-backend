import sys
from flask import Blueprint, request, g
from flask_restful import Api, Resource, abort
from functools import wraps
from marshmallow import ValidationError
from app.accounts import validate_token


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def protected(func):
    @wraps(func)
    def protected_function(*args, **kwargs):
        try:
            token = request.headers['Authorization'] or None

            if not token:
                abort(401, message='Unauthorized', status='error')

            g.current_account = validate_token(token.replace("Bearer ", ""))
            if not g.current_account:
                abort(401, message='Unauthorized', status='error')
        except Exception:
            error_type, error_instance, traceback = sys.exc_info()
            print(str(error_type))
            print(str(error_instance))
            abort(401, message='Unauthorized', status='error')

        return func(*args, **kwargs)

    return protected_function


class ProtectedResource(Resource):
    method_decorators = [protected]


def add_resources():
    from .resources.account import (AccountResource,
                                    AccountListResource,
                                    AccountRoleResource,
                                    RoleResource,
                                    RolesResource)
    from .resources.token import TokenResource, ValidateTokenResource
    from .resources.device import (DeviceResource,
                                   DeviceRecordingResource,
                                   DeviceListResource,
                                   DeviceTypeResource,
                                   DeviceTypeListResource,
                                   DeviceConfigurationResource)
    from .resources.dashboard import DashboardResource, DashboardListResource

    api.add_resource(AccountResource, '/v1/accounts/<int:account_id>')
    api.add_resource(AccountListResource, '/v1/accounts')
    api.add_resource(AccountRoleResource, '/v1/accounts/<int:account_id>/role')
    api.add_resource(RoleResource, '/v1/roles/<int:role_id>')
    api.add_resource(RolesResource, '/v1/roles')
    api.add_resource(TokenResource, '/v1/token')
    api.add_resource(ValidateTokenResource, '/v1/token/validate')
    api.add_resource(DeviceResource, '/v1/devices/<int:device_id>')
    api.add_resource(DeviceRecordingResource,
                     '/v1/devices/<int:device_id>/recordings')
    api.add_resource(DeviceListResource, '/v1/devices')
    api.add_resource(DeviceTypeResource,
                     '/v1/devices/types/<int:device_type_id>')
    api.add_resource(DeviceTypeListResource, '/v1/devices/types')
    api.add_resource(DeviceConfigurationResource,
                     '/v1/devices/<int:device_id>/configuration')
    api.add_resource(DashboardListResource, '/v1/dashboards')
    api.add_resource(DashboardResource,
                     '/v1/dashboards/<int:dashboard_id>')


add_resources()


@api_bp.errorhandler(ValidationError)
@api_bp.errorhandler(422)
def handle_validation_error(e):
    return {'status': 'error', 'message': str(e)}, 422


@api_bp.errorhandler(Exception)
def handle_unknown_errors(e):
    return ({
        'status': 'failed',
        'message': 'Unknown error has occurred! ({0})'.format(str(e))
        }, 500)
