import os
import typing as T
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import yaml


class DeletionMethod(Enum):
    lru = "lru"


@dataclass(frozen=True)
class Config:
    base_path: Path
    max_size: T.Optional[int] = None
    ttl: T.Optional[int] = None
    deletion_method: DeletionMethod = DeletionMethod.lru
    force: bool = False
    disable: bool = False

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
    def load(cls, base_path: Path = None) -> "Config":
        if base_path is None:
            # Search '.scrat' folder starting from the CWD and walking up
            base_path = Path(os.getcwd()) / ".scrat"
            while not os.path.isdir(base_path) and base_path.parent != base_path:
                base_path = base_path.parent
            # TODO: better error messages
            if not os.path.isdir(base_path):
                raise ValueError("couldn't find folder")

        with open(base_path / cls._config_file) as f:
            config_dict = yaml.load(f, Loader=yaml.Loader)

        return cls(
            base_path=Path(config_dict["base_path"]),
            max_size=config_dict["max_size"],
            ttl=config_dict["ttl"],
            deletion_method=DeletionMethod(config_dict["deletion_method"]),
            force=os.environ.get("SCRAT_FORCE", False),
            disable=os.environ.get("SCRAT_DISABLE", False),
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

    @property
    def cache_path(self) -> Path:
        return self.base_path / self._cache_dir

    @property
    def db_path(self) -> Path:
        return self.base_path / self._db_file

    @property
    def config_path(self) -> Path:
        return self.base_path / self._config_file

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
