from typing import List

from sqlalchemy.orm import relationship

from .user import UserOrm
from .task import TaskOrm
from .data_file import DataFile

# User ↔ Task
UserOrm.tasks = relationship("TaskOrm", back_populates="user")
TaskOrm.user = relationship("UserOrm", back_populates="tasks")

# User ↔ DataFile
UserOrm.data_files = relationship("DataFile", back_populates="user")
DataFile.user = relationship("UserOrm", back_populates="data_files")

# Task ↔ DataFile
TaskOrm.data_file = relationship("DataFile", back_populates="tasks")
DataFile.tasks = relationship("TaskOrm", back_populates="data_file")