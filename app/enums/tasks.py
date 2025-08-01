from enum import Enum as PyEnum


class TaskStatus(str, PyEnum):
    OFF = "off"
    WAIT = "wait"
    RUN = "run"
    COMPLETED = "completed"
    ERROR = "error"