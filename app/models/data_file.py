from typing import Optional
from uuid import UUID

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum as SQLEnum

from .base import Base
from .mixins.uuid import UUIDMixin
from ..enums import TableStatus


class DataFile(Base, UUIDMixin):
    __tablename__ = "data_files"

    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    path: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[TableStatus] = mapped_column(SQLEnum(TableStatus), default=TableStatus.ACTIVE)

    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)