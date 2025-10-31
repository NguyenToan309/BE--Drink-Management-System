from werkzeug.security import generate_password_hash, check_password_hash
from src.infrastructure.repositories.user_repository import AbstractUserRepository
from src.domain.models.user import User, UserRole

class AuthService:
    def __init__(self, user_repo: AbstractUserRepository):
        self.user_repo = user_repo

    def register(self, name: str, email: str, password: str, role: UserRole = UserRole.CUSTOMER) -> User:
        if self.user_repo.get_by_email(email):
            raise ValueError(f"Email '{email}' đã tồn tại")
        hashed_password = generate_password_hash(password)
        new_user = User(id=None, email=email, password_hash=hashed_password, role=role, name=name)
        return self.user_repo.add(new_user)

    def login(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            raise ValueError("Email hoặc mật khẩu không chính xác")
        return user
