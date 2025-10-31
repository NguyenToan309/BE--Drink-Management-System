from marshmallow import Schema, fields, validate, post_load
from src.domain.models.user import UserRole

class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    role = fields.Str()

    @post_load
    def make_user_role(self, data, **kwargs):
        if 'role' in data:
            try:
                data['role'] = UserRole(data['role'].lower())
            except ValueError:
                raise validate.ValidationError(f"Vai trò không hợp lệ: {data['role']}")
        return data

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(dump_only=True)
    email = fields.Email(dump_only=True)
    role = fields.Method("get_role_name", dump_only=True)
    phone = fields.Str(dump_only=True)
    address = fields.Str(dump_only=True)

    def get_role_name(self, obj):
        return obj.role.value
