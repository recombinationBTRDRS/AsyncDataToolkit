from uuid import uuid4, UUID

from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID


class UUIDMixin:
    @declared_attr
    def id(cls) -> Mapped[UUID]:
        return mapped_column(
            PGUUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
            unique=True,
            nullable=False,
        )