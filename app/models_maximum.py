from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from enum import Enum as PyEnum
import uuid

Base = declarative_base()

class UserRole(PyEnum):
    USER = "user"
    ADMIN = "admin"

class TableStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    PROCESSING = "processing"
    ERROR = "error"


class TableType(PyEnum):
    ORIGINAL = "original"  
    MODIFIED = "modified"  
    ANALYTICS = "analytics"  

class ExportFormat(PyEnum):
    XML = "xml"
    CSV = "csv"
    JSON = "json"
    EXCEL = "excel"

class BaseTable:
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.timezone.utc)
    status = Column(Enum(TableStatus), default=TableStatus.ACTIVE)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    max_original_tables = Column(Integer, default=10)
    max_modified_per_original = Column(Integer, default=3)
    max_analytics_per_table = Column(Integer, default=3)
    
    original_tables = relationship("OriginalTable", back_populates="owner")
    modified_tables = relationship("ModifiedTable", back_populates="owner")
    analytics_tables = relationship("AnalyticsTable", back_populates="owner")

class OriginalTable(Base, BaseTable):
    __tablename__ = 'original_tables'    
    
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", back_populates="original_tables")    
    
    original_filename = Column(String(255))
    file_size = Column(Integer)  
    file_hash = Column(String(64))      
    
    columns_count = Column(Integer)
    rows_count = Column(Integer)
    columns_metadata = Column(JSON)  
    
    storage_path = Column(String(500))
    duckdb_table_name = Column(String(100)) 
    
    modified_tables = relationship("ModifiedTable", back_populates="parent_table", cascade="all, delete-orphan")
    analytics_tables = relationship("AnalyticsTable", back_populates="source_table", cascade="all, delete-orphan")

class ModifiedTable(Base, BaseTable):
    __tablename__ = 'modified_tables'
    
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", back_populates="modified_tables")
    
    parent_table_id = Column(String, ForeignKey('original_tables.id'), nullable=False)
    parent_table = relationship("OriginalTable", back_populates="modified_tables")
    
    columns_count = Column(Integer)
    rows_count = Column(Integer)
    columns_metadata = Column(JSON)
    
    applied_operations = Column(JSON)  # [{"type": "add_column", "params": {...}}, ...]
    
    storage_path = Column(String(500))
    duckdb_table_name = Column(String(100))
    
    analytics_tables = relationship("AnalyticsTable", back_populates="source_modified_table", cascade="all, delete-orphan")

class AnalyticsTable(Base, BaseTable):
    __tablename__ = 'analytics_tables'
    
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)
    owner = relationship("User", back_populates="analytics_tables")
    
    source_table_id = Column(String, ForeignKey('original_tables.id'), nullable=True)
    source_table = relationship("OriginalTable", back_populates="analytics_tables")
    
    source_modified_table_id = Column(String, ForeignKey('modified_tables.id'), nullable=True)
    source_modified_table = relationship("ModifiedTable", back_populates="analytics_tables")
    
    analytics_type = Column(String(50))  # "summary", "pivot", "chart", "custom"
    
    analytics_config = Column(JSON)  
    
    result_data = Column(JSON)  
    columns_metadata = Column(JSON)
    
    storage_path = Column(String(500))
    duckdb_table_name = Column(String(100))

class TableExport(Base):
    __tablename__ = 'table_exports'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    
    table_id = Column(String, nullable=False)  
    table_type = Column(Enum(TableType), nullable=False)
    
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    export_format = Column(Enum(ExportFormat), nullable=False)
    export_config = Column(JSON)  
    
    file_path = Column(String(500))
    file_size = Column(Integer)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    expires_at = Column(DateTime) 
    
    status = Column(String(20), default="pending")  


class OperationLog(Base):
    __tablename__ = 'operation_logs'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    operation_type = Column(String(50))  
    target_table_id = Column(String)
    target_table_type = Column(Enum(TableType))
    
    operation_details = Column(JSON)
    execution_time = Column(Integer)  
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    status = Column(String(20))  