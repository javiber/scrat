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

    db_file: str = "stash.db"
    stash_dir: str = "stash"
    config_file: str = "config.yaml"

    @property
    def stash_path(self) -> Path:
        return self.base_path / self.stash_dir

    @property
    def db_path(self) -> Path:
        return self.base_path / self.db_file

    @property
    def cache_path(self) -> Path:
        return self.base_path / self.stash_dir

    @property
    def config_path(self) -> Path:
        return self.base_path / self.config_file

    # TODO: find a way to automatically save and load to/from yaml
    @classmethod
    def load(cls, base_path: T.Optional[Path] = None) -> "Config":
        if base_path is None:
            # Search '.scrat' folder starting from the CWD and walking up
            base_path = Path(os.getcwd()) / ".scrat"
            while not os.path.isdir(base_path) and base_path.parent != base_path:
                base_path = base_path.parent
            # TODO: better error messages
            if not os.path.isdir(base_path):
                raise ValueError("couldn't find folder")

        with open(base_path / cls.config_file) as f:
            config_dict = yaml.load(f, Loader=yaml.Loader)

        return cls(
            base_path=Path(config_dict["base_path"]),
            max_size=config_dict["max_size"],
            ttl=config_dict["ttl"],
            deletion_method=DeletionMethod(config_dict["deletion_method"]),
            force=(os.getenv("SCRAT_FORCE", "False").lower() in ("true", 1)),
            disable=(os.getenv("SCRAT_DISABLE", "False").lower() in ("true", 1)),
        )

    @classmethod
    def create_config_file(cls, base_path: Path):
        config = cls(base_path=base_path)
        with open(base_path / cls.config_file, "w") as f:
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
