from flask_restful import Resource, abort
from flask import g, render_template, redirect
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from flasgger import swag_from
from app.api.blueprint import api
import app.accounts.api as accounts
from app.accounts.tasks import send_email_task
from app.api.auth_protection import ProtectedResource
from app.api.permission_protection import (requires_permission,
                                           valid_permissions)
from app.api.schemas import BaseResourceSchema
from flask import current_app as app


class UserSchema(BaseResourceSchema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class RoleUpdateSchema(Schema):
    role_id = fields.Integer(required=True, load_only=True, location='json')


def validate_role_permissions(permissions_list):
    return set(permissions_list).issubset(valid_permissions)


class RoleSchema(BaseResourceSchema):
    id = fields.Integer(required=True, location='json')
    display_name = fields.String(required=True, location='json')
    permissions = fields.List(fields.String, required=True,
                              location='json', many=True,
                              validate=validate_role_permissions)


class RoleCreationSchema(Schema):
    display_name = fields.String(required=True, location='json')
    permissions = fields.List(fields.String, required=True,
                              location='json', many=True)


class AccountResource(ProtectedResource):
    @swag_from('swagger/get_account_spec.yaml')
    def get(self, account_id):
        if g.current_account.id == account_id:
            return UserSchema().dump(g.current_account), 200
        abort(403, message='You can only get your own account', status='error')


class RoleResource(ProtectedResource):
    @swag_from('swagger/get_role_spec.yaml')
    def get(self, role_id):
        return RoleSchema().dump(
                accounts.get_role(role_id)), 200


class RolesResource(ProtectedResource):
    @requires_permission('CREATE_ROLE', 'Role creation')
    @use_args(RoleCreationSchema(), locations=('json',))
    @swag_from('swagger/create_role_spec.yaml')
    def post(self, args):
        created_role = accounts.create_role(args['display_name'],
                                            args['permissions'])
        return RoleSchema().dump(created_role), 201

    @swag_from('swagger/get_roles_spec.yaml')
    def get(self):
        return RoleSchema().dump(accounts.get_all_roles(), many=True), 200


class AccountRoleResource(ProtectedResource):
    @use_args(RoleUpdateSchema(), locations=('json',))
    @swag_from('swagger/update_account_role_spec.yaml')
    def put(self, args, account_id):
        if g.current_account.id == account_id:
            abort(403, message='You may not change your own roles',
                  status='error')
        updated_account = accounts.update_account_role(
                account_id, args['role_id'])
        return UserSchema().dump(updated_account), 200


class AccountListResource(Resource):
    @use_args(UserSchema(), locations=('json',))
    @swag_from('swagger/create_account_spec.yaml')
    def post(self, args):
        try:
            created_account, emailtoken = accounts.create_account(
                    args['username'],
                    args['email'],
                    args['password'])
            confirm_url = api.url_for(
                    AccountEmailTokenResource,
                    token=emailtoken, _external=True)
            html = render_template(
                    'activate_mail.html',
                    confirm_url=confirm_url)
            send_email_task.delay(
                    args['email'],
                    'Please confirm your email',
                    html)
            return UserSchema().dump(created_account), 201
        except ValueError:
            abort(422, message='Account already exists', status='error')


class AccountEmailTokenResource(Resource):
    def get(self, token):
        success, email = accounts.confirm_email_token(token)
        if success:
            html = render_template(
                    'welcome_to_iot.html')
            send_email_task.delay(
                    email,
                    'Welcome to IoT!',
                    html)
            return redirect(app.config['FRONTEND_URL'])


class AccountEmailTokenResendResource(Resource):
    @use_args(UserSchema(), locations=('json',))
    def post(self, args):
        return '', 201
