import os
from pathlib import Path

from appdirs import user_cache_dir
from sqlalchemy.sql import exists, select

from elephant.db import Entry, create_db
from elephant.utils import PathLike

from .base import Cacher


class SimpleCacher(Cacher):
    def __init__(self, base_path: PathLike = None) -> None:
        if base_path is None:
            base_path = Path(user_cache_dir()) / "elephant"
        if not isinstance(base_path, Path):
            base_path = Path(base_path)
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

        self.db = create_db(str((self.base_path / "cache.db").absolute()))

    def add(self, hash: str, path: Path) -> int:
        with self.db() as session:
            session.add(
                Entry(
                    hash=hash,
                    path=str(path),
                )
            )
            session.commit()

    def new(self, hash: str) -> Path:
        return self.base_path / hash

    def exists(self, hash):
        with self.db() as session:
            return session.query(exists().where(Entry.hash == hash)).scalar()

    def get(self, hash):
        with self.db() as session:
            return Path(session.scalar(select(Entry).where(Entry.hash == hash)).path)
