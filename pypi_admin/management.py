# -*- coding: utf-8 -*-

"""Console script for pypi-client."""
import os
import sys
import warnings

import click
from click import ClickException

from pypi_admin.collaborators import collaborators_cli
from pypi_admin.events import events_cli
from pypi_admin.exceptions import PypiTwoFactorRequired, PypiKeyringError
from pypi_admin.projects import projects_cli
from pypi_admin.releases import releases_cli
from pypi_admin.session import PypiSession, get_pypirc_login
from pypi_admin.tokens import tokens_cli


ENV_USERNAME_KEY = 'PYPI_USERNAME'
ENV_PASSWORD_KEY = 'PYPI_PASSWORD'


def get_credentials(username: str, password: str, config_file: str):
    if not username and not password:
        username, password = os.environ.get(ENV_USERNAME_KEY), os.environ.get(ENV_PASSWORD_KEY)
    if not username or not password:
        username, password = get_pypirc_login(config_file)
    if not username or not password:
        raise ClickException(
            'Pypi login is required. Credentials are obtained from one of:\n'
            ' * --username / --password parameters\n'
            f' * {ENV_USERNAME_KEY} / {ENV_PASSWORD_KEY} environment names\n'
            ' * ~/.pypi file (configure path using -c)\n'
        )
    return username, password


def session_login(session: PypiSession):
    try:
        session.login()
    except PypiTwoFactorRequired:
        totp_value = click.prompt('Enter TOTP code', type=int)
        session.two_factor(totp_value)
    else:
        assert session.is_authenticated(), "Not authenticated"
    try:
        session.save_session()
    except PypiKeyringError as e:
        warnings.warn(f'Save session is unavailable: {e}')


def session_restore_or_login(session: PypiSession):
    try:
        session.restore_session()
    except PypiKeyringError as e:
        warnings.warn(f'Restore session is unavailable: {e}')
    if not session.is_authenticated():
        session_login(session)


@click.group()
@click.option('--debug/--no-debug', default=None)
@click.option('-c', '--config-file', default="~/.pypirc")
@click.option('-u', '--username', default=None)
@click.option('-p', '--password', default=None)
@click.pass_context
def cli(ctx, debug, config_file, username, password):
    username, password = get_credentials(username, password, config_file)
    if sys.argv[-1] in ctx.help_option_names:
        return
    session = PypiSession(username, password)
    session_restore_or_login(session)
    ctx.obj = {'session': session}


cli.add_command(tokens_cli)
cli.add_command(projects_cli)
cli.add_command(releases_cli)
cli.add_command(collaborators_cli)
cli.add_command(events_cli)
