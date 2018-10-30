from flask_restful import abort
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from flasgger import swag_from
from flask import g, request
import app.devices.api as devices
from app.api.auth_protection import ProtectedResource
from app.api.schemas import BaseResourceSchema


class BasicDeviceTypeSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)


class DeviceTypeSchema(BaseResourceSchema, BasicDeviceTypeSchema):
    pass


class DeviceSchema(BaseResourceSchema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    device_type = fields.Nested(BasicDeviceTypeSchema, dump_only=True)
    device_type_id = fields.Integer(load_only=True, missing=1)


class DeviceWithConfigurationSchema(DeviceSchema):
    configuration = fields.Raw(dump_only=True)


class RecordingsSchema(BaseResourceSchema):
    recorded_at = fields.DateTime()
    record_type = fields.Integer()
    record_value = fields.Float()


class RecordingsQuerySchema(Schema):
    selections = fields.Raw()
    filters = fields.Raw()
    groups = fields.Raw()
    orders = fields.Raw()


class DeviceSecretSchema(BaseResourceSchema):
    device_secret = fields.String(dump_only=True)
    secret_algorithm = fields.String()


def validate_device_ownership(device_id):
    if not devices.can_user_access_device(g.current_account.id, device_id):
        abort(403, message='You are not allowed to access this device',
              status='error')


class DeviceResource(ProtectedResource):
    @swag_from('swagger/get_device_spec.yaml')
    def get(self, device_id):
        validate_device_ownership(device_id)
        return DeviceWithConfigurationSchema().dump(
                devices.get_device(device_id)), 200

    @swag_from('swagger/delete_device_spec.yaml')
    def delete(self, device_id):
        validate_device_ownership(device_id)
        devices.delete_device(device_id)
        return '', 204


class DeviceTypeResource(ProtectedResource):
    @swag_from('swagger/get_device_type_spec.yaml')
    def get(self, device_type_id):
        return DeviceTypeSchema().dump(
                devices.get_device_type(device_type_id)), 200


class DeviceTypeListResource(ProtectedResource):
    @use_args(DeviceTypeSchema(), locations=('json',))
    @swag_from('swagger/create_device_type_spec.yaml')
    def post(self, args):
        if g.current_account.role_id != 1:
            abort(403, message='Only admin may create device types',
                  status='error')
        created_device_type = devices.create_device_type(
                args['name'])
        return DeviceTypeSchema().dump(created_device_type), 201

    @swag_from('swagger/get_device_types_spec.yaml')
    def get(self):
        return DeviceTypeSchema().dump(devices.get_device_types(),
                                       many=True), 200


class DeviceRecordingResource(ProtectedResource):
    @swag_from('swagger/get_device_recordings_spec.yaml')
    def get(self, device_id):
        validate_device_ownership(device_id)
        request_args = request.args
        return RecordingsSchema().dump(
                    devices.get_device_recordings_filtered(
                        device_id,
                        request_args.get('record_type'),
                        request_args.get('start_date'),
                        request_args.get('end_date')), many=True), 200

    @swag_from('swagger/create_device_recording_spec.yaml')
    def post(self, device_id):
        validate_device_ownership(device_id)
        created_recording = devices.create_recording_and_return(
                device_id, request.json)
        return RecordingsSchema().dump(created_recording), 201


class DeviceRecordingQueryResource(ProtectedResource):
    @use_args(RecordingsQuerySchema(), locations=('json',))
    @swag_from('swagger/create_device_recording_query_spec.yaml')
    def post(self, args, device_id):
        validate_device_ownership(device_id)
        try:
            return {'content':
                    devices.run_custom_query(device_id, args)}, 200
        except ValueError as e:
            abort(400, message=str(e), status='error')


class DeviceListResource(ProtectedResource):
    @use_args(DeviceSchema(), locations=('json',))
    @swag_from('swagger/create_device_spec.yaml')
    def post(self, args):
        created_device = devices.create_device(
                args['name'],
                g.current_account.id,
                args['device_type_id'])
        return DeviceSchema().dump(created_device), 201

    @swag_from('swagger/get_devices_spec.yaml')
    def get(self):
        return DeviceSchema().dump(
                devices.get_devices(g.current_account.id), many=True), 200


class DeviceConfigurationResource(ProtectedResource):
    @swag_from('swagger/update_device_configuration_spec.yaml')
    def put(self, device_id):
        validate_device_ownership(device_id)
        updated_device = devices.set_device_configuration(
                device_id, request.json)
        return DeviceWithConfigurationSchema().dump(
                updated_device), 200

    @swag_from('swagger/get_device_configuration_spec.yaml')
    def get(self, device_id):
        validate_device_ownership(device_id)
        return devices.get_device_configuration(device_id), 200


class DeviceSecretResource(ProtectedResource):
    @swag_from('swagger/get_device_secret_spec.yaml')
    def get(self, device_id):
        validate_device_ownership(device_id)
        return DeviceSecretSchema().dump(devices.get_device(device_id)), 200
