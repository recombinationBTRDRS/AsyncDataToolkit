from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class FileMetadataMixin:
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False)
