import click

from .cache import cache
from .setup import init


@click.group()
def elephant():
    pass


elephant.add_command(init)
elephant.add_command(cache)

if __name__ == "__main__":
    elephant()
