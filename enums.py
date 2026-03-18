from enum import Enum


class UserRole(str, Enum):
    customer = "customer"
    admin = "admin"

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"