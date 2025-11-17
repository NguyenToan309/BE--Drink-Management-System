from flask import Blueprint, jsonify, request
from app import db
from models import Product

product_bp = Blueprint('products', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = [{
        "id": p.id,
        "title": p.title,
        "price": p.price,
        "image_url": p.image_url,
        "stock": p.stock
    } for p in products]
    return jsonify(result)

@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    p = Product.query.get(id)
    if not p:
        return jsonify({"message": "Not found"}), 404
    return jsonify({
        "id": p.id, "title": p.title, "price": p.price,
        "description": p.description, "image_url": p.image_url
    })

@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    p = Product(**data)
    db.session.add(p)
    db.session.commit()
    return jsonify({"message": "Product added", "id": p.id})
