import typing as T
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Nut(Base):
    __tablename__ = "nut"
    hash: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    path: Mapped[str]

    created_at: Mapped[datetime]
    used_at: Mapped[T.Optional[datetime]]
    size: Mapped[int]
    use_count: Mapped[int]
    time_s: Mapped[int]

    def __repr__(self) -> str:
        return f"Nut(hash={self.hash!r}, path={self.path!r})"
