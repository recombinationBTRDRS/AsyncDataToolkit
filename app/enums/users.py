from enum import Enum as PyEnum


class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"
