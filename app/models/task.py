from uuid import UUID

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Enum as SQLEnum

from .base import Base
from .mixins.uuid import UUIDMixin
from ..enums import TaskStatus


class TaskOrm(Base, UUIDMixin):
    __tablename__ = "tasks"

    command: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.OFF)

    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    data_file_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("data_files.id"), nullable=False)