import typing as T
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class Entry(Base):
    __tablename__ = "entry"
    hash: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    path: Mapped[str]

    created_at: Mapped[datetime]
    used_at: Mapped[T.Optional[datetime]]
    size_mb: Mapped[int]
    use_count: Mapped[int]
    time_s: Mapped[int]

    def __repr__(self) -> str:
        return f"Entry(hash={self.hash!r}, path={self.path!r})"


def create_db(path):
    engine = create_engine("sqlite:///" + str(path))
    Base.metadata.create_all(engine)

    return sessionmaker(engine)
