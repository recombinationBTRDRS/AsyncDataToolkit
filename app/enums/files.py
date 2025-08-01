from enum import Enum as PyEnum


class TableStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class TableType(str, PyEnum):
    ORIGINAL = "original"
    MODIFIED = "modified"
    ANALYTICS = "analytics"


