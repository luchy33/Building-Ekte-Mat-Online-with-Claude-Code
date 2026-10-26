from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from app.models.enums import DeliveryMethod, EventType, OrderStatus, PaymentStatus


@dataclass
class GuestGroup:
    guest_count: int
    label: Optional[str] = None
    diet_notes: Optional[str] = None
    id: Optional[int] = None
    order_id: Optional[int] = None


@dataclass
class OrderLine:
    food_item_id: int
    quantity: int
    unit_price_nok: int  # copied from the food item when the order is placed
    id: Optional[int] = None
    order_id: Optional[int] = None

    @property
    def total_nok(self) -> int:
        return self.quantity * self.unit_price_nok


@dataclass
class Order:
    order_number: str
    customer_id: int
    event_type: EventType
    event_date: date
    delivery_method: DeliveryMethod
    delivery_address: Optional[str] = None
    status: OrderStatus = OrderStatus.SUBMITTED
    payment_status: PaymentStatus = PaymentStatus.NOT_PAID
    created_at: datetime = field(default_factory=datetime.now)
    guest_groups: list[GuestGroup] = field(default_factory=list)
    lines: list[OrderLine] = field(default_factory=list)
    id: Optional[int] = None

    ALLOWED_TRANSITIONS = {
        OrderStatus.SUBMITTED: {OrderStatus.APPROVED, OrderStatus.REJECTED, OrderStatus.CANCELLED},
        OrderStatus.APPROVED: {OrderStatus.IN_PREPARATION, OrderStatus.CANCELLED},
        OrderStatus.IN_PREPARATION: {OrderStatus.DELIVERED},
        OrderStatus.DELIVERED: set(),
        OrderStatus.REJECTED: set(),
        OrderStatus.CANCELLED: set(),
    }

    def can_change_status(self, new_status: OrderStatus) -> bool:
        return new_status in self.ALLOWED_TRANSITIONS[self.status]

    def change_status(self, new_status: OrderStatus) -> None:
        if not self.can_change_status(new_status):
            raise ValueError(f"Cannot change order status from {self.status.value} to {new_status.value}")
        self.status = new_status

    @property
    def total_nok(self) -> int:
        return sum(line.total_nok for line in self.lines)

    @property
    def guest_count(self) -> int:
        return sum(group.guest_count for group in self.guest_groups)
