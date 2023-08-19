import typing as T
from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Nut(Base):
    """Represents an entry to the stash database"""

    __tablename__ = "nut"

    # TODO: hash should not be the PK because it could be repeated with a different name
    hash: Mapped[str] = mapped_column(primary_key=True)
    "Resulting hash for this result"
    name: Mapped[str]
    "Name of the function that produced this result"
    path: Mapped[str]
    "Path where the result is stored"

    created_at: Mapped[datetime]
    "DateTime when the result was produced"
    used_at: Mapped[T.Optional[datetime]]
    "DateTime when the result was last used"
    size: Mapped[int]
    "Size of the store file, in bytes"
    use_count: Mapped[int]
    "Count of how many times the result was used"
    time_s: Mapped[int]
    "Execution time of the function, in seconds"

    def __repr__(self) -> str:
        return f"Nut(name={self.name!r}, hash={self.hash!r})"
