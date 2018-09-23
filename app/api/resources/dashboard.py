from flask import g
from flask_restful import abort
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.dashboard as dashboard
from app.api import ProtectedResource


class DashboardSchema(Schema):
    id = fields.Integer(dump_only=True)
    dashboard_data = fields.Raw()


class DashboardWrapperSchema(Schema):
    dashboard = fields.Nested(DashboardSchema, required=True, location='json')


class DashboardsSchema(Schema):
    dashboards = fields.Nested(DashboardSchema, required=True, location='json',
                               many=True)


class DashboardResource(ProtectedResource):
    @swag_from('swagger/get_dashboard_spec.yaml')
    def get(self, dashboard_id):
        requested_dashboard = dashboard.get_dashboard(dashboard_id)
        if requested_dashboard.account_id != g.current_account.id:
            abort(403, message='You are not allowed to access this dashboard',
                  status='error')
        return DashboardWrapperSchema().dump(
                {'dashboard': requested_dashboard}), 200

    @use_args(DashboardWrapperSchema())
    @swag_from('swagger/update_dashboard_spec.yaml')
    def put(self, args, dashboard_id):
        requested_dashboard = dashboard.get_dashboard(dashboard_id)
        if requested_dashboard.account_id != g.current_account.id:
            abort(403, message='You are not allowed to access this dashboard',
                  status='error')
        args = args['dashboard']
        success = dashboard.update_dashboard(
                dashboard_id,
                args['dashboard_data'])
        if success:
            return '', 204


class DashboardListResource(ProtectedResource):
    @use_args(DashboardWrapperSchema())
    @swag_from('swagger/create_dashboard_spec.yaml')
    def post(self, args):
        args = args['dashboard']
        success = dashboard.create_dashboard(
                args['dashboard_data'],
                g.current_account.id)
        if success:
            return '', 201

    @swag_from('swagger/get_dashboards_spec.yaml')
    def get(self):
        return DashboardsSchema().dump(
                {'dashboards':
                    dashboard.get_dashboards(g.current_account.id)}), 200
