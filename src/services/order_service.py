from typing import List, Dict, Optional
from src.domain.models.order import Order, OrderItem, OrderStatus
from src.infrastructure.repositories.order_repository import AbstractOrderRepository
from src.infrastructure.repositories.product_repository import AbstractProductRepository
from src.infrastructure.repositories.user_repository import AbstractUserRepository

class OrderService:
    def __init__(self, order_repo: AbstractOrderRepository, product_repo: AbstractProductRepository, user_repo: AbstractUserRepository):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.user_repo = user_repo

    def create_order(self, customer_id: str, items: List[Dict], delivery_info: Dict) -> Order:
        customer = self.user_repo.get_by_id(customer_id)
        if not customer:
            raise ValueError("Khách hàng không tồn tại")
        domain_items = []
        for item_data in items:
            product = self.product_repo.get_by_id(item_data['product_id'])
            if not product:
                raise ValueError(f"Sản phẩm ID {item_data['product_id']} không tồn tại")
            domain_items.append(OrderItem(
                id=None, order_id=None, product_id=product.id,
                quantity=item_data['quantity'], price_at_order=product.price
            ))
        new_order = Order(
            id=None, customer_id=customer_id, status=OrderStatus.PENDING, created_at=None,
            customer_name=delivery_info['name'], customer_phone=delivery_info['phone'],
            customer_address=delivery_info['address'], items=domain_items
        )
        return self.order_repo.add(new_order)

    def get_order_history(self, customer_id: str) -> List[Order]:
        return self.order_repo.get_by_user_id(customer_id)

    def get_all_pending_orders(self) -> List[Order]:
        # Placeholder. Extend repository to support listing by status system-wide.
        return []

    def update_order_status(self, order_id: str, new_status: OrderStatus) -> Optional[Order]:
        return self.order_repo.update_status(order_id, new_status)
