from enum import Enum


class OrderStatus(str, Enum):
    SUBMITTED = "submitted"
    APPROVED = "approved"
    IN_PREPARATION = "in_preparation"
    DELIVERED = "delivered"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class PaymentStatus(str, Enum):
    NOT_PAID = "not_paid"
    DEPOSIT_PAID = "deposit_paid"
    INVOICED = "invoiced"
    PAID = "paid"


class EventType(str, Enum):
    LUNCH_MEETING = "lunch_meeting"
    PARTY = "party"
    WEDDING_DINNER = "wedding_dinner"
    OTHER = "other"


class DeliveryMethod(str, Enum):
    DELIVERY = "delivery"
    PICK_UP = "pick_up"
