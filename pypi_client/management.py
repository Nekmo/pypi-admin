# -*- coding: utf-8 -*-

"""Console script for pypi-client."""
import sys
import click

from pypi_client.session import PypiSession
from pypi_client.tokens import tokens_cli


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.pass_context
def cli(ctx, debug):
    session = PypiSession()
    if sys.argv[-1] not in ctx.help_option_names:
        session.login()
    ctx.obj = {'session': session}


cli.add_command(tokens_cli)
