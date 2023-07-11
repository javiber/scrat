from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# TODO: persist DB
engine = create_engine("sqlite://", echo=True)


class Base(DeclarativeBase):
    pass


# class Cache(Base):
#     __tablename__ = "cache"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[Optional[str]]
#     location: Mapped[Optional[str]]

#     def __repr__(self) -> str:
#         return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Entry(Base):
    __tablename__ = "entry"
    hash: Mapped[str] = mapped_column(primary_key=True)
    # cache: Mapped["Cache"] = relationship()
    # name: Mapped[str]
    path: Mapped[str]
    # created_at: Mapped[datetime]
    # created_at: Mapped[datetime]
    # size: Mapped[int]

    def __repr__(self) -> str:
        return f"Entry(hash={self.hash!r}, path={self.path!r})"


Base.metadata.create_all(engine)

Session = sessionmaker(engine)
