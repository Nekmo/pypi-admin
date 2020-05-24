import click
from bs4 import BeautifulSoup

from pypi_client.exceptions import PypiTokenUnavailable
from click_default_group import DefaultGroup


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

    def get_by_name(self, name: str) -> Token:
        try:
            return next(filter(lambda x: x.name == name, self.all()))
        except StopIteration:
            raise PypiTokenUnavailable

    def get_by_token_id(self, token_id: str) -> Token:
        try:
            return next(filter(lambda x: x.token_id == token_id, self.all()))
        except StopIteration:
            raise PypiTokenUnavailable

    def create(self, name: str, scope: str = 'scope:user'):
        response = self.session.form_request('/manage/account/token/', {
            'description': name,
            'token_scope': scope,
        })
        soup = BeautifulSoup(response.text)
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


@click.group(cls=DefaultGroup, default='all', default_if_no_args=True)
@click.pass_context
def tokens(ctx):
    """
    """
    session = ctx.obj['session']
    ctx.obj['tokens'] = Tokens(session)


@tokens.command('all')
@click.pass_context
def all_tokens(ctx, **kwargs):
    print(list(ctx.obj['tokens'].all()))
