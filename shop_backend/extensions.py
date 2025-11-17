# shop_backend/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Tạo các instance ở đây
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()