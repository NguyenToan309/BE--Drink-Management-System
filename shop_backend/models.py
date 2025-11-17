# shop_backend/models.py

from extensions import db  # <-- SỬA DÒNG NÀY
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    # Thêm mối quan hệ: một User có nhiều Order
    orders = db.relationship('Order', backref='customer', lazy=True)

# ----------------------------------------------------
# CÁC MODEL MỚI CHO ĐƠN HÀNG
# ----------------------------------------------------

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    
    # Thông tin người nhận
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    payment = db.Column(db.String(50), nullable=False)

    # Liên kết với User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Liên kết với các món hàng
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    
    # Tùy chọn (options)
    size = db.Column(db.String(10), nullable=True)
    sugar = db.Column(db.String(10), nullable=True)
    ice = db.Column(db.String(10), nullable=True)
    topping = db.Column(db.String(50), nullable=True)

    # Liên kết với Đơn hàng
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)