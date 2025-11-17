# shop_backend/routes/order.py

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, OrderItem, User
from extensions import db
from datetime import datetime

order_bp = Blueprint('order', __name__)

# --- API ĐẶT HÀNG ---
@order_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    current_user_id = get_jwt_identity()
    data = request.get_json()

    # Lấy thông tin từ frontend
    info = data.get('info')
    items = data.get('items')
    total = data.get('total')

    if not info or not items or not total:
        return jsonify({"message": "Thiếu thông tin đơn hàng"}), 400

    try:
        # 1. Tạo đơn hàng (Order)
        new_order = Order(
            user_id=current_user_id,
            time=datetime.utcnow(),
            total=total,
            name=info.get('name'),
            phone=info.get('phone'),
            address=info.get('address'),
            payment=info.get('payment')
        )
        db.session.add(new_order)
        db.session.commit() # Commit để lấy được new_order.id

        # 2. Thêm các món hàng (OrderItem) vào đơn hàng
        for item in items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_name=item.get('name'),
                price=item.get('price'),
                qty=item.get('qty'),
                size=item.get('size'),
                sugar=item.get('sugar'),
                ice=item.get('ice'),
                topping=item.get('topping')
            )
            db.session.add(order_item)

        # 3. Commit tất cả các món hàng
        db.session.commit()
        
        return jsonify({"message": "Đặt hàng thành công!", "order_id": new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Lỗi máy chủ", "error": str(e)}), 500


# --- API LẤY LỊCH SỬ ĐƠN HÀNG ---
@order_bp.route('/order-history', methods=['GET'])
@jwt_required()
def get_order_history():
    current_user_id = get_jwt_identity()
    
    # Lấy các đơn hàng CỦA RIÊNG user này, sắp xếp mới nhất lên trước
    user_orders = Order.query.filter_by(user_id=current_user_id).order_by(Order.time.desc()).all()

    # Chuyển đổi dữ liệu sang JSON
    orders_list = []
    for order in user_orders:
        items_list = []
        for item in order.items:
            items_list.append({
                "name": item.product_name,
                "qty": item.qty,
                "price": item.price,
                "size": item.size,
                "sugar": item.sugar,
                "ice": item.ice,
                "topping": item.topping
            })
        
        orders_list.append({
            "id": "KH" + str(order.id), # Giống format cũ
            "time": order.time.strftime("%Y-%m-%d %H:%M:%S"),
            "total": order.total,
            "info": {
                "name": order.name,
                "phone": order.phone,
                "address": order.address,
                "payment": order.payment
            },
            "items": items_list
        })

    return jsonify(orders_list), 200