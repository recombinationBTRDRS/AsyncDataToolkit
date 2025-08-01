from typing import List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON


class FileHeaderMixin:
    headers: Mapped[List[str]] = mapped_column(JSON, nullable=False)
