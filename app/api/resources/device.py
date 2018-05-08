from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.devices as devices
from app.api import ProtectedResource


class DeviceSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class DeviceWrapperSchema(Schema):
    device = fields.Nested(DeviceSchema, required=True, location='json')


class RecordingsSchema(Schema):
    recorded_at = fields.DateTime()
    record_type = fields.Integer()
    record_value = fields.String()


class RecordingsWrapperSchema(Schema):
    recordings = fields.Nested(RecordingsSchema, required=True,
                               location='json', many=True)


class DeviceResource(ProtectedResource):
    @swag_from('swagger/get_device_spec.yaml')
    def get(self, device_id):
        return DeviceWrapperSchema().dump(
                {'device': devices.get_device(device_id)}), 200


class DeviceRecordingResource(ProtectedResource):
    @swag_from('swagger/get_device_recordings_spec.yaml')
    def get(self, device_id):
        return RecordingsWrapperSchema().dump(
                {'recordings': devices.get_device_recordings(device_id)}), 200


class DeviceListResource(ProtectedResource):
    @use_args(DeviceWrapperSchema())
    @swag_from('swagger/create_device_spec.yaml')
    def post(self, args):
        args = args['device']
        success = devices.create_device(
                args['name'])
        if success:
            return '', 201
