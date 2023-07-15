import os
import typing as T
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

import yaml
from sqlalchemy.sql import exists, select

from elephant.db import Entry, create_db
from elephant.utils import PathLike


class DeletionMethod(Enum):
    lru = "lru"


@dataclass(frozen=True)
class CacheConfig:
    base_path: Path
    max_size: T.Optional[int] = None
    ttl: T.Optional[int] = None
    deletion_method: DeletionMethod = DeletionMethod.lru

    _db_file: str = "cache.db"
    _cache_dir: str = "cache"
    _config_file: str = "config.yaml"

    @property
    def cache_path(self) -> Path:
        return self.base_path / self._cache_dir

    @property
    def db_path(self) -> Path:
        return self.base_path / self._db_file

    # TODO: find a way to automatically save and load to/from yaml
    @classmethod
    def load(cls, base_path: Path) -> "CacheConfig":
        with open(base_path / cls._config_file) as f:
            config_dict = yaml.load(f, Loader=yaml.Loader)
        return cls(
            base_path=Path(config_dict["base_path"]),
            max_size=config_dict["max_size"],
            ttl=config_dict["ttl"],
            deletion_method=DeletionMethod(config_dict["deletion_method"]),
        )

    @classmethod
    def create_config_file(cls, base_path: Path, *args, **kwargs):
        config = cls(base_path=base_path, *args, **kwargs)
        with open(base_path / cls._config_file, "w") as f:
            yaml.dump(
                {
                    "base_path": str(config.base_path.absolute()),
                    "max_size": config.max_size,
                    "ttl": config.ttl,
                    "deletion_method": config.deletion_method.value,
                },
                f,
            )
        return config


class CacheManager:
    # CacheManager is a singleton
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.config: CacheConfig = self._load_config()
        self.db = create_db(self.config.db_path)

    def _load_config(self):
        base_dir = Path(os.getcwd()) / ".elephant"
        while not os.path.isdir(base_dir) and base_dir.parent != base_dir:
            base_dir = base_dir.parent

        if not os.path.isdir(base_dir):
            raise ValueError("couldn't find folder")

        return CacheConfig.load(base_path=base_dir)

    def add(self, entry: Entry) -> int:
        with self.db() as session:
            session.add(entry)
            session.commit()

    def new(self, hash: str) -> Path:
        return self.config.cache_path / hash

    def exists(self, hash):
        with self.db() as session:
            return session.query(exists().where(Entry.hash == hash)).scalar()

    def get(self, hash) -> Entry:
        with self.db() as session:
            return session.scalar(select(Entry).where(Entry.hash == hash))

    def update_usage(self, entry: Entry):
        with self.db() as session:
            session.query(Entry).where(Entry.hash == entry.hash).update(
                {Entry.use_count: entry.use_count + 1, Entry.used_at: datetime.now()},
                synchronize_session=False,
            )
            session.commit()

    def new_entry(
        cls,
        hash: str,
        name: str,
        path: str,
        time_s: int,
    ) -> Entry:
        file_size = round(os.stat(path).st_size)

        return Entry(
            hash=hash,
            name=name,
            path=path,
            created_at=datetime.now(),
            used_at=None,
            size=file_size,
            use_count=0,
            time_s=time_s,
        )
