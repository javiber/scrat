import os
from datetime import timedelta
from pathlib import Path

import click

from elephant.cache import CacheConfig, CacheManager
from elephant.db import Entry, create_db


def make_config(path) -> CacheConfig:
    return CacheConfig.create_config_file(base_path=path)


def make_db(path):
    create_db(path=path)


@click.command()
def init():
    folder = Path(os.getcwd()) / ".elephant"

    if os.path.exists(folder):
        click.secho("already initialized", fg="red")
        exit(-1)

    os.mkdir(folder)
    config = make_config(folder)
    make_db(config.db_path)
    os.mkdir(folder / "cache")

    # TODO: add to gitignore


if __name__ == "__main__":
    init()
