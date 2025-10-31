from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.models.order import Order, OrderItem, OrderStatus
from src.infrastructure.models.order import OrderModel, OrderItemModel
from src.infrastructure.models._db import db

class AbstractOrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> Order: ...
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> List[Order]: ...
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]: ...
    @abstractmethod
    def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]: ...

class SqlOrderRepository(AbstractOrderRepository):
    def _to_domain_item(self, model: OrderItemModel) -> OrderItem:
        return OrderItem(
            id=model.id,
            order_id=model.order_id,
            product_id=model.product_id,
            quantity=model.quantity,
            price_at_order=model.price_at_order
        )

    def _to_domain_order(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            customer_id=model.customer_id,
            status=model.status,
            created_at=model.created_at,
            customer_name=model.customer_name,
            customer_phone=model.customer_phone,
            customer_address=model.customer_address,
            items=[self._to_domain_item(item) for item in model.items]
        )

    def add(self, order: Order) -> Order:
        new_order_model = OrderModel(
            customer_id=order.customer_id,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            customer_address=order.customer_address,
            status=OrderStatus.PENDING
        )
        for item in order.items:
            db.session.add(OrderItemModel(
                order=new_order_model,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_order=item.price_at_order
            ))
        db.session.add(new_order_model)
        db.session.commit()
        return self._to_domain_order(new_order_model)

    def get_by_user_id(self, user_id: str) -> List[Order]:
        models = OrderModel.query.filter_by(customer_id=user_id).order_by(OrderModel.created_at.desc()).all()
        return [self._to_domain_order(m) for m in models]

    def get_by_id(self, order_id: str) -> Optional[Order]:
        m = OrderModel.query.get(order_id)
        return self._to_domain_order(m) if m else None

    def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        m = OrderModel.query.get(order_id)
        if not m:
            return None
        m.status = status
        db.session.commit()
        return self._to_domain_order(m)
