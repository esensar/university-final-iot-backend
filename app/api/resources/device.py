from flask_restful import abort
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from flasgger import swag_from
from flask import g, request
import app.devices as devices
from app.api import ProtectedResource


class DeviceTypeSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class DeviceSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    device_type = fields.Nested(DeviceTypeSchema, dump_only=True)
    device_type_id = fields.Integer(load_only=True, missing=1)


class DeviceWithConfigurationSchema(DeviceSchema):
    configuration = fields.Raw(dump_only=True)


class DeviceWrapperSchema(Schema):
    device = fields.Nested(DeviceWithConfigurationSchema,
                           required=True, location='json')


class DevicesWrapperSchema(Schema):
    devices = fields.Nested(DeviceSchema, required=True,
                            location='json', many=True)


class DeviceTypeWrapperSchema(Schema):
    device_type = fields.Nested(DeviceTypeSchema, required=True,
                                location='json')


class DeviceTypesWrapperSchema(Schema):
    device_types = fields.Nested(DeviceTypeSchema, required=True,
                                 location='json', many=True)


class RecordingsSchema(Schema):
    recorded_at = fields.DateTime()
    record_type = fields.Integer()
    record_value = fields.String()


class RecordingsWrapperSchema(Schema):
    recordings = fields.Nested(RecordingsSchema, required=True,
                               location='json', many=True)


def validate_device_ownership(device_id):
    if not devices.can_user_access_device(g.current_account.id, device_id):
        abort(403, message='You are not allowed to access this device',
              status='error')


class DeviceResource(ProtectedResource):
    @swag_from('swagger/get_device_spec.yaml')
    def get(self, device_id):
        validate_device_ownership(device_id)
        return DeviceWrapperSchema().dump(
                {'device': devices.get_device(device_id)}), 200

    @swag_from('swagger/delete_device_spec.yaml')
    def delete(self, device_id):
        validate_device_ownership(device_id)
        devices.delete_device(device_id)
        return '', 204


class DeviceTypeResource(ProtectedResource):
    @swag_from('swagger/get_device_type_spec.yaml')
    def get(self, device_type_id):
        return DeviceTypeWrapperSchema().dump(
                {'device_type': devices.get_device_type(device_type_id)}), 200


class DeviceTypeListResource(ProtectedResource):
    @use_args(DeviceTypeWrapperSchema())
    @swag_from('swagger/create_device_type_spec.yaml')
    def post(self, args):
        if g.current_account.role_id != 1:
            abort(403, message='Only admin may create device types',
                  status='error')
        args = args['device_type']
        success = devices.create_device_type(
                args['name'])
        if success:
            return '', 201

    @swag_from('swagger/get_device_types_spec.yaml')
    def get(self):
        return DeviceTypesWrapperSchema().dump(
                {'device_types': devices.get_device_types()}), 200


class DeviceRecordingResource(ProtectedResource):
    @swag_from('swagger/get_device_recordings_spec.yaml')
    def get(self, device_id):
        validate_device_ownership(device_id)
        return RecordingsWrapperSchema().dump(
                {'recordings': devices.get_device_recordings(device_id)}), 200


class DeviceListResource(ProtectedResource):
    @use_args(DeviceWrapperSchema())
    @swag_from('swagger/create_device_spec.yaml')
    def post(self, args):
        args = args['device']
        success = devices.create_device(
                args['name'],
                g.current_account.id,
                args['device_type_id'])
        if success:
            return '', 201

    @swag_from('swagger/get_devices_spec.yaml')
    def get(self):
        return DevicesWrapperSchema().dump(
                {'devices': devices.get_devices(g.current_account.id)}), 200


class DeviceConfigurationResource(ProtectedResource):
    @swag_from('swagger/update_device_configuration_spec.yaml')
    def put(self, device_id):
        validate_device_ownership(device_id)
        success = devices.set_device_configuration(device_id, request.json)
        if success:
            return '', 204

    @swag_from('swagger/get_device_configuration_spec.yaml')
    def get(self, device_id):
        validate_device_ownership(device_id)
        return devices.get_device_configuration(device_id), 200
