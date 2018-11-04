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


class MqttConfigResource(ProtectedResource):
    @swag_from('swagger/get_mqtt_config_spec.yaml')
    def get(self):
        return MqttConfigSchema().dump({
            'broker': get_mqtt_broker_info(app.config),
            'endpoints':  get_mqtt_endpoints(app.config)
        }), 200
