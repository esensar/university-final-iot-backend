from flask import g, request
from flask_restful import abort
from marshmallow import fields, Schema
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.dashboards.api as dashboard
from app.api.auth_protection import ProtectedResource
from app.api.schemas import BaseResourceSchema


class DashboardSchema(BaseResourceSchema):
    id = fields.Integer(dump_only=True)
    active = fields.Boolean(required=False)
    dashboard_data = fields.Raw()


class DashboardIdSchema(Schema):
    id = fields.Integer()


class DashboardResource(ProtectedResource):
    @swag_from('swagger/get_dashboard_spec.yaml')
    def get(self, dashboard_id):
        requested_dashboard = dashboard.get_dashboard(dashboard_id)
        if requested_dashboard.account_id != g.current_account.id:
            abort(403, message='You are not allowed to access this dashboard',
                  status='error')
        return DashboardSchema().dump(requested_dashboard), 200

    @use_args(DashboardSchema(), locations=('json',))
    @swag_from('swagger/update_dashboard_spec.yaml')
    def put(self, args, dashboard_id):
        requested_dashboard = dashboard.get_dashboard(dashboard_id)
        if requested_dashboard.account_id != g.current_account.id:
            abort(403, message='You are not allowed to access this dashboard',
                  status='error')
        if args.get('dashboard_data') is None:
            abort(400, message='Missing dashboard_data', status='error')
        if args.get('active') is None:
            abort(400, message='Missing active', status='error')
        success = dashboard.patch_dashboard(
                g.current_account.id,
                dashboard_id,
                args['dashboard_data'],
                args['active'])
        if success:
            return '', 204

    @use_args(DashboardSchema(), locations=('json',))
    @swag_from('swagger/update_dashboard_spec.yaml')
    def patch(self, args, dashboard_id):
        requested_dashboard = dashboard.get_dashboard(dashboard_id)
        if requested_dashboard.account_id != g.current_account.id:
            abort(403, message='You are not allowed to access this dashboard',
                  status='error')
        success = dashboard.patch_dashboard(
                g.current_account.id,
                dashboard_id,
                args.get('dashboard_data'),
                args.get('active'))
        if success:
            return '', 204

    @swag_from('swagger/delete_dashboard_spec.yaml')
    def delete(self, dashboard_id):
        requested_dashboard = dashboard.get_dashboard(dashboard_id)
        if requested_dashboard.account_id != g.current_account.id:
            abort(403, message='You are not allowed to access this dashboard',
                  status='error')
        dashboard.delete_dashboard(dashboard_id)
        return '', 204


class DashboardListResource(ProtectedResource):
    @use_args(DashboardSchema(), locations=('json',))
    @swag_from('swagger/create_dashboard_spec.yaml')
    def post(self, args):
        success = dashboard.create_dashboard(
                args['dashboard_data'],
                g.current_account.id)
        if success:
            return '', 201

    @swag_from('swagger/get_dashboards_spec.yaml')
    def get(self):
        request_args = request.args
        return DashboardSchema().dump(
                dashboard.get_dashboards(
                    g.current_account.id,
                    request_args.get('active')), many=True), 200
