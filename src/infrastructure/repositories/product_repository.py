from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.product import Product
from src.infrastructure.models.product import ProductModel
from src.infrastructure.models._db import db

class AbstractProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Product]: ...
    @abstractmethod
    def get_by_id(self, product_id: str) -> Optional[Product]: ...
    @abstractmethod
    def add(self, product: Product) -> Product: ...
    @abstractmethod
    def update(self, product: Product) -> Product: ...
    @abstractmethod
    def delete(self, product_id: str): ...

class SqlProductRepository(AbstractProductRepository):
    def _to_domain(self, model: ProductModel) -> Product:
        return Product(id=model.id, name=model.name, price=model.price)

    def get_all(self) -> List[Product]:
        return [self._to_domain(p) for p in ProductModel.query.all()]

    def get_by_id(self, product_id: str) -> Optional[Product]:
        p = ProductModel.query.get(product_id)
        return self._to_domain(p) if p else None

    def add(self, product: Product) -> Product:
        new_db_product = ProductModel(name=product.name, price=product.price)
        db.session.add(new_db_product)
        db.session.commit()
        return self._to_domain(new_db_product)

    def update(self, product: Product) -> Product:
        db_product = ProductModel.query.get(product.id)
        if not db_product:
            raise ValueError("Product not found")
        db_product.name = product.name
        db_product.price = product.price
        db.session.commit()
        return self._to_domain(db_product)

    def delete(self, product_id: str):
        db_product = ProductModel.query.get(product_id)
        if not db_product:
            raise ValueError("Product not found")
        db.session.delete(db_product)
        db.session.commit()
