import click
from click_default_group import DefaultGroup

from pypi_admin.table import Table


class Collaborator:
    def __init__(self, collaborators: 'Collaborators', avatar: str, username: str, role: str):
        self.collaborators = collaborators
        self.avatar = avatar
        self.username = username
        self.role = role


class Collaborators:
    def __init__(self, session, project):
        self.session = session
        self.project = project

    def all(self):
        soup = self.session.soup_request(f'/manage/project/{self.project}/collaboration/')
        table = soup.find('table', class_='table--collaborators').find('tbody')
        for row in table.find_all('tr'):
            avatar = row.find('img').attrs['src']
            username = row.find('strong').text
            role = next(row.find('td').stripped_strings)
            yield Collaborator(self, avatar, username, role)


@click.group(name='collaborators', cls=DefaultGroup, default='all')
@click.argument('project')
@click.pass_context
def collaborators_cli(ctx, project):
    """
    """
    session = ctx.obj['session']
    ctx.obj['collaborators'] = Collaborators(session, project)


@collaborators_cli.command('all')
@click.pass_context
def all_collaborators(ctx, **kwargs):
    rows = [[collaborator.username, collaborator.role]
            for collaborator in ctx.obj['collaborators'].all()]
    click.echo(str(Table(['Username', 'Role'], rows)))
