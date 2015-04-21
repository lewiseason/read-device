import click

from ..config import Config
from ..helpers import set_exception_handler

pass_config = click.make_pass_decorator(Config)

@click.command()
def main():
  print('Hello World')
