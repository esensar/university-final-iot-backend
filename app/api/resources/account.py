from flask_restful import Resource, abort
from flask import g
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from flasgger import swag_from
import app.accounts as accounts
from app.api import ProtectedResource, requires_permission


class UserSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class RoleUpdateSchema(Schema):
    role_id = fields.Integer(required=True, load_only=True, location='json')


class RoleSchema(Schema):
    id = fields.Integer(required=True, location='json')
    display_name = fields.String(required=True, location='json')
    permissions = fields.List(fields.String, required=True,
                              location='json', many=True)


class RoleWrapperSchema(Schema):
    role = fields.Nested(RoleSchema, required=True, location='json')


class RolesWrapperSchema(Schema):
    roles = fields.Nested(RoleSchema, required=True,
                          location='json', many=True)


class RoleCreationSchema(Schema):
    display_name = fields.String(required=True, location='json')
    permissions = fields.List(fields.String, required=True,
                              location='json', many=True)


class RoleCreationWrapperSchema(Schema):
    role = fields.Nested(RoleCreationSchema, required=True, location='json')


class UserWrapperSchema(Schema):
    user = fields.Nested(UserSchema, required=True, location='json')


class AccountResource(ProtectedResource):
    @swag_from('swagger/get_account_spec.yaml')
    def get(self, account_id):
        if g.current_account.id == account_id:
            return UserWrapperSchema().dump({'user': g.current_account}), 200
        abort(403, message='You can only get your own account', status='error')


class RoleResource(ProtectedResource):
    @swag_from('swagger/get_role_spec.yaml')
    def get(self, role_id):
        return RoleWrapperSchema().dump(
                {'role': accounts.get_role(role_id)}), 200


class RolesResource(ProtectedResource):
    @requires_permission('CREATE_ROLE', 'Role creation')
    @use_args(RoleCreationWrapperSchema())
    @swag_from('swagger/create_role_spec.yaml')
    def post(self, args):
        args = args['role']
        success = accounts.create_role(args['display_name'],
                                       args['permissions'])
        if success:
            return '', 201

    @swag_from('swagger/get_roles_spec.yaml')
    def get(self):
        return RolesWrapperSchema().dump(
                {'roles': accounts.get_all_roles()}), 200


class AccountRoleResource(ProtectedResource):
    @use_args(RoleUpdateSchema())
    @swag_from('swagger/update_account_role_spec.yaml')
    def put(self, args, account_id):
        if g.current_account.id == account_id:
            abort(403, message='You may not change your own roles',
                  status='error')
        success = accounts.update_account_role(account_id, args['role_id'])
        if success:
            return '', 204


class AccountListResource(Resource):
    @use_args(UserWrapperSchema())
    @swag_from('swagger/create_account_spec.yaml')
    def post(self, args):
        try:
            args = args['user']
            success = accounts.create_account(
                    args['username'],
                    args['email'],
                    args['password'])
            if success:
                return '', 201
        except ValueError:
            abort(422, message='Account already exists', status='error')
