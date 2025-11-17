from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import CartItem, Product

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()
    result = []
    for i in items:
        p = Product.query.get(i.product_id)
        result.append({
            "product_id": p.id,
            "title": p.title,
            "price": p.price,
            "quantity": i.quantity
        })
    return jsonify(result)

@cart_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    item = CartItem.query.filter_by(user_id=user_id, product_id=data['product_id']).first()
    if item:
        item.quantity = data['quantity']
    else:
        item = CartItem(user_id=user_id, product_id=data['product_id'], quantity=data['quantity'])
        db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Cart updated"})
