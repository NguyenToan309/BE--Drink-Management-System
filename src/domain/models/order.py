import dataclasses
from typing import List
from datetime import datetime
from enum import Enum

class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclasses.dataclass
class OrderItem:
    id: str
    order_id: str
    product_id: str
    quantity: int
    price_at_order: float

@dataclasses.dataclass
class Order:
    id: str
    customer_id: str
    status: OrderStatus
    created_at: datetime
    customer_name: str
    customer_phone: str
    customer_address: str
    items: List[OrderItem]
    total_price: float = 0.0

    def __post_init__(self):
        self.total_price = sum(item.quantity * item.price_at_order for item in self.items)
