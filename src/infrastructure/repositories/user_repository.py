from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models.user import User, UserRole
from src.infrastructure.models.user import UserModel
from src.infrastructure.models._db import db

class AbstractUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User: ...
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: ...
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]: ...

class SqlUserRepository(AbstractUserRepository):
    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            role=model.role,
            name=model.name,
            phone=model.phone,
            address=model.address
        )

    def add(self, user: User) -> User:
        new_user_model = UserModel(
            email=user.email,
            password_hash=user.password_hash,
            role=user.role,
            name=user.name,
            phone=user.phone,
            address=user.address
        )
        db.session.add(new_user_model)
        db.session.commit()
        return self._to_domain(new_user_model)

    def get_by_email(self, email: str) -> Optional[User]:
        model = UserModel.query.filter_by(email=email).first()
        return self._to_domain(model) if model else None

    def get_by_id(self, user_id: str) -> Optional[User]:
        model = UserModel.query.get(user_id)
        return self._to_domain(model) if model else None
