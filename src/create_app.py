from flask import Flask
from src.dependency_container import AppContainer
from src.infrastructure.models._db import db

# Import các blueprint
from src.api.controllers.product_controller import create_product_blueprint 
from src.api.controllers.auth_controller import create_auth_blueprint
from src.api.controllers.customer_controller import create_customer_blueprint

def create_app() -> Flask:
    app = Flask(__name__)

    # === CẤU HÌNH MYSQL ===
    # Cú pháp đúng với mysqlclient: 'mysql+mysqldb://TEN_DANG_NHAP:MAT_KHAU@TEN_HOST/TEN_DATABASE'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:123456@localhost/drink_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    container = AppContainer()
    app.container = container 

    # === Lấy các controller từ container ===
    product_controller = container.product_controller()
    auth_controller = container.auth_controller()
    customer_controller = container.customer_controller()

    # === Đăng ký tất cả blueprint ===
    product_blueprint = create_product_blueprint(product_controller)
    auth_blueprint = create_auth_blueprint(auth_controller)
    customer_blueprint = create_customer_blueprint(customer_controller)

    app.register_blueprint(product_blueprint, url_prefix='/api/manager')
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(customer_blueprint, url_prefix='/api/customer')

    # Tạo các bảng CSDL (nếu chưa có)
    with app.app_context():
        db.create_all()

    return app
