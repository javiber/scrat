import os
from pathlib import Path

import click

from elephant.cache import CacheManager
from elephant.db import Entry, create_db


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
                entry.used_at,
                str(entry.size_mb),
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


cache.add_command(list)
cache.add_command(clear)


if __name__ == "__main__":
    cache()
