from flask import Blueprint, request, jsonify
from src.services.product_service import ProductService
from src.api.schemas.product_schema import ProductSchema
from marshmallow import ValidationError

class ProductController:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
        self.product_schema = ProductSchema()
        self.products_schema = ProductSchema(many=True)

    def get_all(self):
        products = self.product_service.get_all_products()
        return jsonify(self.products_schema.dump(products)), 200

    def create(self):
        try:
            data = self.product_schema.load(request.json)
            new_product = self.product_service.create_product(name=data['name'], price=data['price'])
            return jsonify(self.product_schema.dump(new_product)), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

    def update(self, product_id):
        try:
            data = self.product_schema.load(request.json)
            updated_product = self.product_service.update_product(product_id, data['name'], data['price'])
            if updated_product is None:
                return jsonify({"error": "Sản phẩm không tìm thấy"}), 404
            return jsonify(self.product_schema.dump(updated_product)), 200
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

    def delete(self, product_id):
        success = self.product_service.delete_product(product_id)
        if not success:
            return jsonify({"error": "Sản phẩm không tìm thấy"}), 404
        return "", 204

def create_product_blueprint(controller: ProductController) -> Blueprint:
    blueprint = Blueprint('manager_products', __name__)
    blueprint.add_url_rule('/products', view_func=controller.get_all, methods=['GET'])
    blueprint.add_url_rule('/products', view_func=controller.create, methods=['POST'])
    blueprint.add_url_rule('/products/<string:product_id>', view_func=controller.update, methods=['PUT'])
    blueprint.add_url_rule('/products/<string:product_id>', view_func=controller.delete, methods=['DELETE'])
    return blueprint
