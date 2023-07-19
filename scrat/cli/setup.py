import os
from pathlib import Path

import click

from scrat import Config
from scrat.db import DBConnector


def _make_config(path) -> Config:
    return Config.create_config_file(base_path=path)


def _make_db(path):
    DBConnector.create_db(path=path)


@click.command()
def init():
    """Initialize Scrat's stash"""
    cwd = Path(os.getcwd())
    folder = cwd / ".scrat"

    if os.path.exists(folder):
        click.secho("already initialized", fg="red")
        exit(-1)

    os.mkdir(folder)
    config = _make_config(folder)
    _make_db(config.db_path)
    os.mkdir(config.stash_path)

    if os.path.exists(cwd / ".git"):
        with open(folder / ".gitignore", "w") as f:
            f.write(f"{config.stash_dir}\n{config.db_file}\n{config.config_file}\n")


@click.command()
def deinit():
    """Remove Scrat's stash"""
    import shutil

    cwd = Path(os.getcwd())
    folder = cwd / ".scrat"

    if not os.path.exists(folder):
        click.secho("not initialized", fg="red")
        exit(-1)
    click.confirm(
        "This will remove everything from the stash are you sure?", abort=True
    )
    shutil.rmtree(folder)
    click.secho("Scrat was deinitialized correctly")


if __name__ == "__main__":
    init()
