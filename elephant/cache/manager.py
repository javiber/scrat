import os
import typing as T
from dataclasses import dataclass
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
    def cache_path(self) -> str:
        return self.base_path / self._cache_dir

    @property
    def db_path(self) -> str:
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
    def init(cls, base_path: Path, *args, **kwargs):
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
        return self.config.cache_path / hash

    def exists(self, hash):
        with self.db() as session:
            return session.query(exists().where(Entry.hash == hash)).scalar()

    def get(self, hash):
        with self.db() as session:
            return Path(session.scalar(select(Entry).where(Entry.hash == hash)).path)
