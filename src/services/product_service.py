from typing import List, Optional
from src.domain.models.product import Product
from src.infrastructure.repositories.product_repository import AbstractProductRepository

class ProductService:
    def __init__(self, product_repo: AbstractProductRepository):
        self.product_repo = product_repo

    def get_all_products(self) -> List[Product]:
        return self.product_repo.get_all()

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        return self.product_repo.get_by_id(product_id)

    def create_product(self, name: str, price: float) -> Product:
        if price <= 0:
            raise ValueError("Giá sản phẩm phải là số dương.")
        new_product = Product(id=None, name=name, price=price)
        return self.product_repo.add(new_product)

    def update_product(self, product_id: str, name: str, price: float) -> Optional[Product]:
        product_to_update = self.get_product_by_id(product_id)
        if product_to_update is None:
            return None
        if price <= 0:
            raise ValueError("Giá sản phẩm phải là số dương.")
        product_to_update.name = name
        product_to_update.price = price
        return self.product_repo.update(product_to_update)

    def delete_product(self, product_id: str) -> bool:
        try:
            self.product_repo.delete(product_id)
            return True
        except ValueError:
            return False
