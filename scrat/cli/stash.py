import os
from datetime import timedelta

import click
from sqlalchemy.sql import exists, select

from scrat.config import Config
from scrat.db import DBConnector, Entry
from scrat.utils import humanize_size


@click.group()
def stash():
    pass


COLUMNS = [
    "hash",
    "name",
    "path",
    "created_at",
    "used_at",
    "size_mb",
    "use_count",
    "time_s",
]


def format_datetime(datetime):
    if datetime is not None:
        return datetime.isoformat(timespec="minutes", sep=" ")
    return ""


@stash.command()
@click.option(
    "-s",
    "--sort-by",
    type=click.Choice(COLUMNS),
    default="created_at",
    help="Column to sort by",
)
@click.option(
    "-d", "--desc", default=False, is_flag=True, help="Use to sort descending"
)
def list(sort_by, desc):
    """List content of stash"""
    config = Config.load()
    db_connector = DBConnector(config.db_path)
    with db_connector.session() as session:
        sorting = getattr(Entry, sort_by)
        if desc:
            sorting = sorting.desc()
        click.secho(f"{'name':<10} {'hash':<32} {'created_at':<16} {'size':5}")

        for entry in session.query(Entry).order_by(sorting).all():
            click.secho(
                (
                    f"{entry.name:<10} {entry.hash} "
                    f"{format_datetime(entry.created_at)} "
                    f"{humanize_size(entry.size)}"
                )
            )


@stash.command()
@click.argument("hash_key", help="the hash of the entry to remove")
def delete(hash_key):
    """Removes one entry from the stash"""
    config = Config.load()
    db_connector = DBConnector(config.db_path)
    with db_connector.session() as session:
        entry = session.scalar(select(Entry).where(Entry.hash == hash_key))
        if entry is None:
            click.secho("Entry does not exists", fg="red")
            exit(-1)
        try:
            os.remove(entry.path)
        except FileNotFoundError:
            pass
        session.query(Entry).filter_by(hash=hash_key).delete()
        session.commit()


@stash.command()
def clear():
    """Empty the stash"""
    config = Config.load()
    click.confirm(
        "This will remove everything from the stash are you sure?", abort=True
    )
    try:
        os.remove(config.db_path)
    except FileNotFoundError:
        click.secho("DB not found")
    for file in os.listdir(config.cache_path):
        os.remove(config.cache_path / file)


@stash.command()
def stats():
    """Print stash stats"""
    config = Config.load()
    db_connector = DBConnector(config.db_path)
    seconds_saved = 0
    size = 0
    entries = 0
    with db_connector.session() as session:
        for entry in session.query(Entry).all():
            seconds_saved += entry.use_count * entry.time_s
            size += entry.size
            entries += 1

    click.secho(f"Total entries: {entries}")
    if entries == 0:
        return

    click.secho(f"Total size: {humanize_size(size)}")

    if seconds_saved > 0:
        click.secho(f"time saved: {timedelta(seconds=seconds_saved)}")


@stash.command()
def check():
    """Check the integrity of the stash"""
    config = Config.load()
    db_connector = DBConnector(config.db_path)
    with db_connector.session() as session:
        for entry in session.query(Entry).all():
            if not os.path.exists(entry.path):
                click.secho(f"Missing file '{entry.hash}'")
        for file in os.listdir(config.cache_path):
            if not session.query(exists().where(Entry.hash == file)).scalar():
                click.secho(f"File not indexed: '{file}'")


if __name__ == "__main__":
    stash()
