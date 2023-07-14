import os
from datetime import timedelta
from pathlib import Path

import click
from sqlalchemy.sql import exists

from elephant.cache import CacheManager
from elephant.db import Entry
from elephant.utils import humanize_size


@click.group()
def cache():
    pass


@click.command()
def list():
    from rich.console import Console
    from rich.table import Table

    table = Table(title="Entries")
    table.add_column("hash")
    table.add_column("name")
    table.add_column("path")
    table.add_column("created_at")
    table.add_column("used_at")
    table.add_column("size_mb")
    table.add_column("use_count")
    table.add_column("time_s")

    cache_manager = CacheManager()
    with cache_manager.db() as session:
        for entry in session.query(Entry).all():
            table.add_row(
                entry.hash,
                entry.name,
                entry.path,
                entry.created_at.isoformat(),
                entry.used_at.isoformat() if entry.used_at is not None else "None",
                str(entry.size),
                str(entry.use_count),
                str(entry.time_s),
            )

    console = Console()
    console.print(table)


@click.command()
def clear():
    cache_manager = CacheManager()
    os.remove(cache_manager.config.db_path)
    for file in os.listdir(cache_manager.config.cache_path):
        os.remove(cache_manager.config.cache_path / file)


@click.command()
def stats():
    cache_manager = CacheManager()
    seconds_saved = 0
    size = 0
    entries = 0
    with cache_manager.db() as session:
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


@click.command()
def check():
    cache_manager = CacheManager()
    with cache_manager.db() as session:
        for entry in session.query(Entry).all():
            if not os.path.exists(entry.path):
                click.secho(f"Missing file '{entry.hash}'")
        for file in os.listdir(cache_manager.config.cache_path):
            if not session.query(exists().where(Entry.hash == file)).scalar():
                click.secho(f"File not indexed: '{file}'")


cache.add_command(list)
cache.add_command(clear)
cache.add_command(stats)
cache.add_command(check)


if __name__ == "__main__":
    cache()
