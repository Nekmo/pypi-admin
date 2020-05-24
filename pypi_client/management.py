# -*- coding: utf-8 -*-

"""Console script for pypi-client."""
import os
import sys
import click
from click import ClickException

from pypi_client.collaborators import collaborators_cli
from pypi_client.events import events_cli
from pypi_client.exceptions import PypiTwoFactorRequired
from pypi_client.projects import projects_cli
from pypi_client.releases import releases_cli
from pypi_client.session import PypiSession, get_pypi_login
from pypi_client.tokens import tokens_cli


ENV_USERNAME_KEY = 'PYPI_USERNAME'
ENV_PASSWORD_KEY = 'PYPI_PASSWORD'


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('-c', '--config-file', default="~/.pypirc")
@click.option('-u', '--username', default=None)
@click.option('-p', '--password', default=None)
@click.pass_context
def cli(ctx, debug, config_file, username, password):
    if not username and not password:
        username, password = os.environ.get(ENV_USERNAME_KEY), os.environ.get(ENV_PASSWORD_KEY)
    if not username or not password:
        username, password = get_pypi_login(config_file)
    if not username or not password:
        raise ClickException(
            'Pypi login is required. Credentials are obtained from one of:\n'
            ' * --username / --password parameters\n'
            f' * {ENV_USERNAME_KEY} / {ENV_PASSWORD_KEY} environment names\n'
            ' * ~/.pypi file (configure path using -c)\n'
        )
    if sys.argv[-1] in ctx.help_option_names:
        return
    session = PypiSession(username, password)
    try:
        session.login()
    except PypiTwoFactorRequired:
        totp_value = click.prompt('Enter TOTP code', type=int)
        session.two_factor(totp_value)
    ctx.obj = {'session': session}


cli.add_command(tokens_cli)
cli.add_command(projects_cli)
cli.add_command(releases_cli)
cli.add_command(collaborators_cli)
cli.add_command(events_cli)
