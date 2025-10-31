import dataclasses
from enum import Enum

class UserRole(Enum):
    CUSTOMER = "customer"
    STAFF = "staff"
    MANAGER = "manager"
    ADMIN = "admin"

@dataclasses.dataclass
class User:
    id: str
    email: str
    password_hash: str  # internal only
    role: UserRole
    name: str = ""
    phone: str = ""
    address: str = ""
