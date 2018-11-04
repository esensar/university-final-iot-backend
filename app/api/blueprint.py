from flask_restful import Api
from marshmallow import ValidationError
from app.errors import NotPresentError, BadRequestError
from flask import Blueprint, jsonify


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


def add_resources():
    from .resources.account import (AccountResource,
                                    AccountListResource,
                                    AccountRoleResource,
                                    RoleResource,
                                    RolesResource,
                                    AccountEmailTokenResource,
                                    AccountEmailTokenResendResource)
    from .resources.token import TokenResource, ValidateTokenResource
    from .resources.device import (DeviceResource,
                                   DeviceRecordingResource,
                                   DeviceRecordingQueryResource,
                                   DeviceListResource,
                                   DeviceTypeResource,
                                   DeviceTypeListResource,
                                   DeviceConfigurationResource,
                                   DeviceSecretResource,
                                   DeviceSecretResetResource,
                                   DeviceShareResource,
                                   DeviceShareActivationResource)
    from .resources.dashboard import (DashboardResource,
                                      DashboardListResource,
                                      DashboardWidgetResource,
                                      DashboardWidgetListResource)
    from .resources.app import MqttConfigResource, AppConfigResource

    api.add_resource(AccountResource, '/v1/accounts/<int:account_id>')
    api.add_resource(AccountListResource, '/v1/accounts')
    api.add_resource(AccountRoleResource, '/v1/accounts/<int:account_id>/role')
    api.add_resource(AccountEmailTokenResource,
                     '/v1/email/confirm/<string:token>')
    api.add_resource(AccountEmailTokenResendResource,
                     '/v1/email/resend')
    api.add_resource(RoleResource, '/v1/roles/<int:role_id>')
    api.add_resource(RolesResource, '/v1/roles')
    api.add_resource(TokenResource, '/v1/token')
    api.add_resource(ValidateTokenResource, '/v1/token/validate')
    api.add_resource(DeviceResource, '/v1/devices/<int:device_id>')
    api.add_resource(DeviceRecordingResource,
                     '/v1/devices/<int:device_id>/recordings')
    api.add_resource(DeviceRecordingQueryResource,
                     '/v1/devices/<int:device_id>/recordings/jsonql')
    api.add_resource(DeviceListResource, '/v1/devices')
    api.add_resource(DeviceTypeResource,
                     '/v1/devices/types/<int:device_type_id>')
    api.add_resource(DeviceTypeListResource, '/v1/devices/types')
    api.add_resource(DeviceConfigurationResource,
                     '/v1/devices/<int:device_id>/configuration')
    api.add_resource(DeviceSecretResource,
                     '/v1/devices/<int:device_id>/secret')
    api.add_resource(DeviceSecretResetResource,
                     '/v1/devices/<int:device_id>/secret/reset')
    api.add_resource(DeviceShareResource,
                     '/v1/devices/<int:device_id>/share')
    api.add_resource(
            DeviceShareActivationResource,
            '/v1/devices/<int:device_id>/share/activate/<string:token>')
    api.add_resource(DashboardResource,
                     '/v1/dashboards/<int:dashboard_id>')
    api.add_resource(DashboardListResource, '/v1/dashboards')
    api.add_resource(
            DashboardWidgetResource,
            '/v1/dashboards/<int:dashboard_id>/widgets/<int:widget_id>')
    api.add_resource(DashboardWidgetListResource,
                     '/v1/dashboards/<int:dashboard_id>/widgets')
    api.add_resource(MqttConfigResource, '/v1/config/mqtt')
    api.add_resource(AppConfigResource, '/v1/config')


add_resources()


@api_bp.errorhandler(ValidationError)
@api_bp.errorhandler(422)
def handle_validation_error(e):
    return jsonify({'status': 'error', 'message': str(e)}), 422


@api_bp.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({'status': 'error', 'message': str(e)}), 422


@api_bp.errorhandler(NotPresentError)
@api_bp.errorhandler(404)
def handle_not_present_error(e):
    return jsonify({'status': 'error', 'message': str(e)}), 404


@api_bp.errorhandler(BadRequestError)
@api_bp.errorhandler(400)
def handle_bad_request_error(e):
    return jsonify({'status': 'error', 'message': str(e)}), 400


@api_bp.errorhandler(Exception)
@api_bp.errorhandler(500)
def handle_unknown_errors(e):
    return jsonify({
        'status': 'failed',
        'message': 'Unknown error has occurred! ({0})'.format(str(e))
        }), 500
