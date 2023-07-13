import click

from .config import init


@click.group()
def elephant():
    pass


elephant.add_command(init)

if __name__ == "__main__":
    elephant()
