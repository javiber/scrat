import os
from pathlib import Path

import click

from scrat import Config
from scrat.db import DBConnector


def make_config(path) -> Config:
    return Config.create_config_file(base_path=path)


def make_db(path):
    DBConnector.create_db(path=path)


@click.command()
def init():
    cwd = Path(os.getcwd())
    folder = cwd / ".scrat"

    if os.path.exists(folder):
        click.secho("already initialized", fg="red")
        exit(-1)

    os.mkdir(folder)
    config = make_config(folder)
    make_db(config.db_path)
    os.mkdir(folder / "cache")

    if os.path.exists(cwd / ".git"):
        with open(folder / ".gitignore", "w") as f:
            f.writelines(["./cache\n" "./cache.db\n"])


if __name__ == "__main__":
    init()
