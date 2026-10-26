from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Question:
    """A question sent from the shop and answered in the admin panel."""
    name: str
    email: str
    subject: str
    body: str
    customer_id: Optional[int] = None
    answer: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    answered_at: Optional[datetime] = None
    id: Optional[int] = None
