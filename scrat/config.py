import os
import typing as T
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import yaml


class CachePolicy(Enum):
    lru = "lru"
    lfu = "lfu"


@dataclass(frozen=True)
class Config:
    base_path: Path
    "path to `.scrat` forlder"
    # TODO: global max_size is not enforced yet
    max_size: T.Optional[int] = None
    "size limit of the stash"
    # TODO: global ttl is not enforced yet
    ttl: T.Optional[int] = None
    "Time-to-live of objects"
    cache_policy: CachePolicy = CachePolicy.lru
    "Cache policy used to remove entries"
    force: bool = False
    "Forcefully re-run all functions"
    disable: bool = False
    "Forcefully re-run all functions but not store the results"

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
        "Load the config from a yaml"
        if base_path is None:
            # Search '.scrat' folder starting from the CWD and walking up
            cwd = Path(os.getcwd())
            while not os.path.isdir(cwd / ".scrat") and cwd.parent != cwd:
                cwd = cwd.parent
            if not os.path.isdir(cwd / ".scrat"):
                raise ValueError("Scrat is not initialized, did you run `scrat init`")
            base_path = cwd / ".scrat"

        with open(base_path / cls.config_file) as f:
            config_dict = yaml.load(f, Loader=yaml.Loader)

        return cls(
            base_path=Path(config_dict["base_path"]),
            max_size=config_dict["max_size"],
            ttl=config_dict["ttl"],
            cache_policy=CachePolicy(config_dict["cache_policy"]),
            force=(os.getenv("SCRAT_FORCE", "False").lower() in ("true", 1)),
            disable=(os.getenv("SCRAT_DISABLE", "False").lower() in ("true", 1)),
        )

    @classmethod
    def create_config_file(cls, base_path: Path):
        "Initialize the yaml with the default settings"
        config = cls(base_path=base_path)
        with open(base_path / cls.config_file, "w") as f:
            yaml.dump(
                {
                    "base_path": str(config.base_path.absolute()),
                    "max_size": config.max_size,
                    "ttl": config.ttl,
                    "cache_policy": config.cache_policy.value,
                },
                f,
            )
        return config
