from flask import Blueprint, request, jsonify
from src.services.auth_service import AuthService
from src.api.schemas.user_schema import RegisterSchema, LoginSchema, UserSchema
from marshmallow import ValidationError

class AuthController:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.register_schema = RegisterSchema()
        self.login_schema = LoginSchema()
        self.user_schema = UserSchema()

    def register(self):
        try:
            data = self.register_schema.load(request.json)
            user = self.auth_service.register(
                name=data['name'], 
                email=data['email'], 
                password=data['password']
            )
            return jsonify(self.user_schema.dump(user)), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

    def login(self):
        try:
            data = self.login_schema.load(request.json)
            user = self.auth_service.login(data['email'], data['password'])
            return jsonify({
                "message": "Đăng nhập thành công", 
                "user": self.user_schema.dump(user)
            }), 200
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

def create_auth_blueprint(controller: AuthController) -> Blueprint:
    blueprint = Blueprint('auth', __name__)
    blueprint.add_url_rule('/register', view_func=controller.register, methods=['POST'])
    blueprint.add_url_rule('/login', view_func=controller.login, methods=['POST'])
    return blueprint
