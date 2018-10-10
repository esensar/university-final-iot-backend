from flask import g
from flask_restful import abort
from marshmallow import fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.dashboards.api as dashboard
from app.api.auth_protection import ProtectedResource
from app.api.schemas import BaseResourceSchema


class DashboardSchema(BaseResourceSchema):
    id = fields.Integer(dump_only=True)
    dashboard_data = fields.Raw()


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
        success = dashboard.update_dashboard(
                dashboard_id,
                args['dashboard_data'])
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
        return DashboardSchema().dump(
                dashboard.get_dashboards(g.current_account.id), many=True), 200
