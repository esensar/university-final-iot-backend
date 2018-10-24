from flask import g, request
from flask_restful import abort
from marshmallow import fields, Schema
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.dashboards.api as dashboard
import app.devices.api as device
from app.api.auth_protection import ProtectedResource
from app.api.schemas import BaseResourceSchema


class BasicDashboardWidgetSchema(Schema):
    id = fields.Integer(dump_only=True)
    device_id = fields.Integer()
    height = fields.Integer()
    width = fields.Integer()
    x = fields.Integer()
    y = fields.Integer()
    chart_type = fields.String()
    filters = fields.Raw()


class DashboardWidgetSchema(BaseResourceSchema, BasicDashboardWidgetSchema):
    pass


class DashboardSchema(BaseResourceSchema):
    id = fields.Integer(dump_only=True)
    active = fields.Boolean(required=False)
    dashboard_data = fields.Raw()
    name = fields.String()
    widgets = fields.Nested(BasicDashboardWidgetSchema, dump_only=True,
                            many=True)


def validate_dashboard_ownership(dashboard_id):
    requested_dashboard = dashboard.get_dashboard(dashboard_id)
    if requested_dashboard.account_id != g.current_account.id:
        abort(403, message='You are not allowed to access this dashboard',
              status='error')
    return requested_dashboard


def validate_device_ownership(device_id):
    if not device.can_user_access_device(g.current_account.id, device_id):
        abort(403, message='You are not allowed to access this device',
              status='error')


class DashboardResource(ProtectedResource):
    @swag_from('swagger/get_dashboard_spec.yaml')
    def get(self, dashboard_id):
        requested_dashboard = validate_dashboard_ownership(dashboard_id)
        return DashboardSchema().dump(requested_dashboard), 200

    @use_args(DashboardSchema(), locations=('json',))
    @swag_from('swagger/update_dashboard_spec.yaml')
    def put(self, args, dashboard_id):
        validate_dashboard_ownership(dashboard_id)
        updated_dashboard = dashboard.patch_dashboard(
                g.current_account.id,
                dashboard_id,
                args['dashboard_data'],
                args['active'],
                args['name'])
        return DashboardSchema().dump(updated_dashboard), 200

    @use_args(DashboardSchema(partial=True), locations=('json',))
    @swag_from('swagger/update_dashboard_spec.yaml')
    def patch(self, args, dashboard_id):
        validate_dashboard_ownership(dashboard_id)
        updated_dashboard = dashboard.patch_dashboard(
                g.current_account.id,
                dashboard_id,
                args.get('dashboard_data'),
                args.get('active'),
                args.get('name'))
        return DashboardSchema().dump(updated_dashboard), 200

    @swag_from('swagger/delete_dashboard_spec.yaml')
    def delete(self, dashboard_id):
        validate_dashboard_ownership(dashboard_id)
        dashboard.delete_dashboard(dashboard_id)
        return '', 204


class DashboardListResource(ProtectedResource):
    @use_args(DashboardSchema(), locations=('json',))
    @swag_from('swagger/create_dashboard_spec.yaml')
    def post(self, args):
        created_dashboard = dashboard.create_dashboard(
                args['dashboard_data'],
                args['name'],
                g.current_account.id)
        return DashboardSchema().dump(created_dashboard), 201

    @swag_from('swagger/get_dashboards_spec.yaml')
    def get(self):
        request_args = request.args
        return DashboardSchema().dump(
                dashboard.get_dashboards(
                    g.current_account.id,
                    request_args.get('active')), many=True), 200


class DashboardWidgetListResource(ProtectedResource):
    @use_args(DashboardWidgetSchema(), locations=('json',))
    @swag_from('swagger/create_dashboard_widget_spec.yaml')
    def post(self, args, dashboard_id):
        validate_dashboard_ownership(dashboard_id)
        validate_device_ownership(args['device_id'])
        created_widget = dashboard.create_widget(
                dashboard_id,
                args['device_id'],
                args['height'],
                args['width'],
                args['x'],
                args['y'],
                args['chart_type'],
                args['filters'])
        return DashboardWidgetSchema().dump(created_widget), 201

    @swag_from('swagger/get_dashboard_widgets_spec.yaml')
    def get(self, dashboard_id):
        validate_dashboard_ownership(dashboard_id)
        return DashboardWidgetSchema().dump(
                dashboard.get_widgets(dashboard_id), many=True), 200


class DashboardWidgetResource(ProtectedResource):
    @swag_from('swagger/get_dashboard_widget_spec.yaml')
    def get(self, dashboard_id, widget_id):
        validate_dashboard_ownership(dashboard_id)
        requested_widget = dashboard.get_widget(widget_id)
        return DashboardWidgetSchema().dump(requested_widget), 200

    @use_args(DashboardWidgetSchema(), locations=('json',))
    @swag_from('swagger/update_dashboard_widget_spec.yaml')
    def put(self, args, dashboard_id, widget_id):
        validate_dashboard_ownership(dashboard_id)
        validate_device_ownership(args['device_id'])
        updated_widget = dashboard.patch_widget(
                widget_id,
                args['device_id'],
                args['height'],
                args['width'],
                args['x'],
                args['y'],
                args['chart_type'],
                args['filters'])
        return DashboardWidgetSchema().dump(updated_widget), 200

    @use_args(DashboardWidgetSchema(partial=True), locations=('json',))
    @swag_from('swagger/update_dashboard_widget_spec.yaml')
    def patch(self, args, dashboard_id, widget_id):
        validate_dashboard_ownership(dashboard_id)
        if args.get('device_id') is not None:
            validate_device_ownership(args['device_id'])
        updated_widget = dashboard.patch_widget(
                widget_id,
                args.get('device_id'),
                args.get('height'),
                args.get('width'),
                args.get('x'),
                args.get('y'),
                args.get('chart_type'),
                args.get('filters'))
        return DashboardWidgetSchema().dump(updated_widget), 200

    @swag_from('swagger/delete_dashboard_widget_spec.yaml')
    def delete(self, dashboard_id, widget_id):
        validate_dashboard_ownership(dashboard_id)
        dashboard.delete_widget(widget_id)
        return '', 204
