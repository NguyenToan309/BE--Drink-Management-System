from ._db import db
from src.domain.models.order import OrderStatus
from datetime import datetime
import uuid

class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_address = db.Column(db.String(255), nullable=False)

    customer = db.relationship('UserModel', back_populates='orders')
    items = db.relationship('OrderItemModel', back_populates='order', cascade="all, delete-orphan", lazy=True)

class OrderItemModel(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)

    order = db.relationship('OrderModel', back_populates='items')
    product = db.relationship('ProductModel', lazy=True)
