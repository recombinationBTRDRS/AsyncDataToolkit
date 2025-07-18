from sqlalchemy.orm import  DeclarativeBase, Mapped, mapped_column, relationship
from typing import Optional, List

from sqlalchemy import ForeignKey, DateTime, JSON, String, Integer, Enum as SQLEnum
from datetime import datetime, timezone


from enum import Enum as PyEnum


class Base(DeclarativeBase):
    pass

class FileMixin:
    __abstract__ = True

    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path:      Mapped[str] = mapped_column(String(512), nullable=False)
    file_size:         Mapped[int] = mapped_column(Integer, nullable=False)
    file_hash:         Mapped[str] = mapped_column(String(64),  nullable=False)

    headers: Mapped[List[str]] = mapped_column(JSON, nullable=False)

class UserRole(PyEnum):
    USER = "user"
    ADMIN = "admin"

class TableStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class TableType(PyEnum):
    ORIGINAL = "original"  
    MODIFIED = "modified"  
    ANALYTICS = "analytics"

class TaskStatus(PyEnum):
    OFF = "off"
    WAIT = "wait"
    RUN = "run"
    COMPLETED = "completed"
    ERROR = "error"

class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    name:Mapped[str]
    role:Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER)
    tasks: Mapped[list["TaskOrm"]] = relationship(back_populates="user")
    original_tables: Mapped[list["OriginalTableORM"]] = relationship(
        back_populates="user"
    )


class BaseTable:
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    name: Mapped[Optional[str]] = mapped_column(nullable=True)
    description : Mapped[Optional[str]] = mapped_column(nullable=True)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc))
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc))   
    status: Mapped[TableStatus] = mapped_column(SQLEnum(TableStatus), default=TableStatus.ACTIVE)
    columns_count: Mapped[int] = mapped_column(Integer, nullable=False)
    rows_count: Mapped[int]    = mapped_column(Integer, nullable=False)


class OriginalTableORM(Base, BaseTable, FileMixin):
    __tablename__ = "original_tables"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    user: Mapped["UserOrm"] = relationship(back_populates="original_tables")
    tasks: Mapped[list["TaskOrm"]] = relationship(back_populates="original_table")
    
        

class TaskOrm(Base):
    __tablename__ = "task"

    id :Mapped[int] = mapped_column(primary_key=True,index=True)
    command : Mapped[str]  = mapped_column(String(255), nullable=False)
    status : Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.OFF)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserOrm"] = relationship(back_populates="tasks")
    table_id: Mapped[int] = mapped_column(ForeignKey("original_tables.id"))
    original_table: Mapped["OriginalTableORM"] = relationship(back_populates="tasks")

