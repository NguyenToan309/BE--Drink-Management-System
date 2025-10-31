from flask import Blueprint, request, jsonify
from src.services.order_service import OrderService
from src.services.product_service import ProductService
from src.api.schemas.order_schema import CreateOrderSchema, OrderOutputSchema
from src.api.schemas.product_schema import ProductSchema
from marshmallow import ValidationError

class CustomerController:
    def __init__(self, order_service: OrderService, product_service: ProductService):
        self.order_service = order_service
        self.product_service = product_service
        self.create_order_schema = CreateOrderSchema()
        self.order_output_schema = OrderOutputSchema()
        self.orders_output_schema = OrderOutputSchema(many=True)
        self.products_schema = ProductSchema(many=True)

    def get_menu(self):
        products = self.product_service.get_all_products()
        return jsonify(self.products_schema.dump(products)), 200

    def create_order(self):
        try:
            data = self.create_order_schema.load(request.json)
            order = self.order_service.create_order(
                customer_id=data['customer_id'],
                items=data['items'],
                delivery_info=data['delivery_info']
            )
            return jsonify(self.order_output_schema.dump(order)), 201
        except ValidationError as err:
            return jsonify({"errors": err.messages}), 400
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

    def get_order_history(self, customer_id):
        orders = self.order_service.get_order_history(customer_id)
        return jsonify(self.orders_output_schema.dump(orders)), 200

def create_customer_blueprint(controller: CustomerController) -> Blueprint:
    blueprint = Blueprint('customer', __name__)
    blueprint.add_url_rule('/menu', view_func=controller.get_menu, methods=['GET'])
    blueprint.add_url_rule('/orders', view_func=controller.create_order, methods=['POST'])
    blueprint.add_url_rule('/orders/history/<string:customer_id>', view_func=controller.get_order_history, methods=['GET'])
    return blueprint
