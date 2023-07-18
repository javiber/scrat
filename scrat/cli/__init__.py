import click

from .setup import init
from .stash import stash


@click.group()
def scrat():
    pass


scrat.add_command(init)
scrat.add_command(stash)

if __name__ == "__main__":
    scrat()
