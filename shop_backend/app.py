# shop_backend/app.py

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

# Import các extensions
from extensions import db, bcrypt, jwt

# Import CẢ HAI blueprints
from routes.auth import auth_bp
from routes.orders import order_bp # <-- (THÊM DÒNG NÀY)

def create_app():
    app = Flask(__name__, static_folder=None)

    # Cấu hình
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'

    # Khởi tạo các extension đã import
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Bật CORS
    CORS(app) 

    # Đăng ký CẢ HAI blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api') # <-- (THÊM DÒNG NÀY)

    # Tạo DB nếu chưa có
    with app.app_context():
        # ----------------------------------------------------
        # (PHẢI IMPORT CÁC MODEL VÀO ĐÂY)
        # ----------------------------------------------------
        from models import User, Order, OrderItem 
        db.create_all()

    # Serve frontend
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../shop_frontend')

    @app.route('/')
    def index():
        return send_from_directory(frontend_dir, 'login.html')

    @app.route('/<path:path>')
    def static_proxy(path):
        return send_from_directory(frontend_dir, path)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=4000, debug=True)