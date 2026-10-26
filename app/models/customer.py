from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class Customer:
    """A customer account. Admins are customers with is_admin=True (simplification of StaffUser)."""
    name: str
    email: str
    customer_type: str = "private"  # "private" or "corporate"
    phone: Optional[str] = None
    organisation_number: Optional[str] = None
    password_hash: str = ""
    is_admin: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return bool(self.password_hash) and check_password_hash(self.password_hash, password)
