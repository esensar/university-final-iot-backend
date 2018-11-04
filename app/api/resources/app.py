from flask import current_app as app
from marshmallow import Schema, fields
from flasgger import swag_from
from app.api.auth_protection import ProtectedResource
from app.api.schemas import BaseResourceSchema


class BasicMqttBrokerSchema(Schema):
    url = fields.String()
    port = fields.String()


class MqttBrokerSchema(BaseResourceSchema, BasicMqttBrokerSchema):
    pass


class BasicMqttEndpointSchema(Schema):
    topic = fields.String()
    description = fields.String()
    body_example = fields.Raw()


class MqttEndpointSchema(BaseResourceSchema, BasicMqttEndpointSchema):
    pass


class MqttConfigSchema(BaseResourceSchema):
    broker = fields.Nested(BasicMqttBrokerSchema)
    endpoints = fields.Nested(BasicMqttEndpointSchema, many=True)


class BasicVersionInfoSchema(Schema):
    name = fields.String()
    build_number = fields.String()


class VersionInfoSchema(BaseResourceSchema, BasicVersionInfoSchema):
    pass


class BasicFrontendInfoSchema(Schema):
    url = fields.String()


class FrontendInfoSchema(BaseResourceSchema, BasicFrontendInfoSchema):
    pass


class BasicEmailInfoSchema(Schema):
    mailer_account = fields.String()
    contact_accounts = fields.List(fields.String, many=True)


class EmailInfoSchema(BaseResourceSchema, BasicEmailInfoSchema):
    pass


class AppConfigSchema(BaseResourceSchema):
    version = fields.Nested(BasicVersionInfoSchema)
    frontend = fields.Nested(BasicFrontendInfoSchema)
    email = fields.Nested(BasicEmailInfoSchema)


def get_mqtt_broker_info(config):
    return {
        'url': config['MQTT_BROKER_URL'],
        'port': config['MQTT_BROKER_PORT']
    }


def get_mqtt_endpoints(config):
    return [
        {
            'topic': 'device/<device_id>',
            'description': 'Used by devices to send data to server. ' +
                           'All messages sent to this endpoint must be in ' +
                           'JSON format and signed with device secret (sign' +
                           'ature should be added to original JSON after ' +
                           'signing as "hmac" key in root object). JSON can ' +
                           'contain any number of keys, but there are a few ' +
                           'mandatory fields.',
            'body_example': {
                'record_type': 1,
                'record_value': 123,
                'recorded_at': 1537379424,
                'hmac': "jfdhslfh12383j12l3j12oirjfkdsfd"
            }
        },
        {
            'topic': 'device/<device_id>/config',
            'description': 'Used by server to send config to ' +
                           'devices. Devices should listen to this endpoint ' +
                           'in order to properly receive updated ' +
                           'configuration.',
            'body_example': {
                'update_rate': 4,
                'mode': 'passive'
            }
        }
    ]


def get_app_version_info(config):
    return {
        'name': config['APP_VERSION'],
        'build_number': config['APP_RELEASE_VERSION_STRING']
    }


def get_frontend_info(config):
    return {
        'url': config['FRONTEND_URL']
    }


def get_email_info(config):
    return {
        'mailer_account': config['MAIL_DEFAULT_SENDER'],
        'contact_accounts': config['MAIL_CONTACT_ACCOUNTS']
    }


class MqttConfigResource(ProtectedResource):
    @swag_from('swagger/get_mqtt_config_spec.yaml')
    def get(self):
        return MqttConfigSchema().dump({
            'broker': get_mqtt_broker_info(app.config),
            'endpoints':  get_mqtt_endpoints(app.config)
        }), 200


class AppConfigResource(ProtectedResource):
    @swag_from('swagger/get_app_config_spec.yaml')
    def get(self):
        return AppConfigSchema().dump({
            'version': get_app_version_info(app.config),
            'frontend': get_frontend_info(app.config),
            'email': get_email_info(app.config)
        }), 200
