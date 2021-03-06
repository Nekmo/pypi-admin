import sys
from typing import Iterable, Union

import click
from bs4 import BeautifulSoup

from pypi_admin.exceptions import PypiTokenUnavailable
from click_default_group import DefaultGroup

from pypi_admin.table import Table


class Token:
    def __init__(self, tokens: 'Tokens', name: str, token_id: str, created, token=None):
        self.tokens = tokens
        self.name = name
        self.token_id = token_id
        self.created = created
        self.token = token

    def delete(self):
        self.tokens.delete(self.token_id)

    def __repr__(self):
        return f'<Token "{str(self)}">'

    def __str__(self):
        return self.name


class Tokens:
    def __init__(self, session):
        self.session = session

    def all(self):
        soup = self.session.soup_request('/manage/account/')
        section = soup.find('section', id='api-tokens').find('tbody')
        for row in section.find_all('tr'):
            name = list(row.find('th').stripped_strings)[1]
            token_id = row.find('input', attrs={'name': 'macaroon_id'}).attrs['value']
            created = row.find('time').attrs['datetime']
            yield Token(self, name, token_id, created)

    def get(self, name_or_id: str) -> Token:
        tokens = list(self.all())
        try:
            return self.get_by_token_id(name_or_id, tokens)
        except PypiTokenUnavailable:
            pass
        return self.get_by_name(name_or_id)

    def get_by_name(self, name: str, tokens: Union[Iterable[Token], None] = None) -> Token:
        tokens = tokens or self.all()
        try:
            return next(filter(lambda x: x.name == name, tokens))
        except StopIteration:
            raise PypiTokenUnavailable

    def get_by_token_id(self, token_id: str, tokens: Union[Iterable[Token], None] = None) -> Token:
        tokens = tokens or self.all()
        try:
            return next(filter(lambda x: x.token_id == token_id, tokens))
        except StopIteration:
            raise PypiTokenUnavailable

    def create(self, name: str, scope: str = 'scope:user'):
        response = self.session.form_request('/manage/account/token/', {
            'description': name,
            'token_scope': scope,
        })
        soup = BeautifulSoup(response.text, 'html.parser')
        provisioned = soup.find('section', id='provisioned-key')
        code = provisioned.find('code', class_='code-block')
        token_id = provisioned.find('input', attrs={'name': 'macaroon_id'}).attrs['value']
        return Token(
            self, name, token_id, None, code.text
        )

    def delete(self, token_id: str):
        self.session.form_request('/manage/account/token/', {
            'macaroon_id': token_id,
            'confirm_password': self.session.password,
        }, original_path='/manage/account/')


@click.group(name='tokens', cls=DefaultGroup, default='all', default_if_no_args=True)
@click.pass_context
def tokens_cli(ctx):
    """
    """
    session = ctx.obj['session']
    ctx.obj['tokens'] = Tokens(session)


@tokens_cli.command('all')
@click.pass_context
def all_tokens(ctx, **kwargs):
    rows = [[token.name, token.token_id, token.created]
            for token in ctx.obj['tokens'].all()]
    click.echo(str(Table(['Name', 'Token ID', 'Created'], rows)))


@tokens_cli.command('create')
@click.argument('name')
@click.argument('scope', default='')
@click.pass_context
def create_token(ctx, name, scope=''):
    scope = f'scope:project:{scope}' if scope else 'scope:user'
    tokens: Tokens = ctx.obj['tokens']
    token: Token = tokens.create(name, scope)
    if sys.stdout.isatty():
        click.echo(
            'For security reasons this token will only appear once:'
            f'\n\n{token.token}\n\n'
            f'Use this token to upload {name or "any"} package\n\n'
            f'Token id: {token.name}\n'
            f'Token name: {token.token_id}'
        )
    else:
        sys.stdout.write(token.token)


@tokens_cli.command('delete')
@click.argument('name_or_id')
@click.pass_context
def delete_token(ctx, name_or_id):
    tokens: Tokens = ctx.obj['tokens']
    token = tokens.get(name_or_id)
    token.delete()
    click.echo(f'Deleted token {token.name} ({token.token_id})')
