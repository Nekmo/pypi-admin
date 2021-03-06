import click
from click_default_group import DefaultGroup

from pypi_admin.table import Table


class Release:
    def __init__(self, releases: 'Releases', version: str, released: str):
        self.releases = releases
        self.version = version
        self.released = released


class Releases:
    def __init__(self, session, project):
        self.session = session
        self.project = project

    def all(self):
        soup = self.session.soup_request(f'/manage/project/{self.project}/releases/')
        table = soup.find('table', class_='table--releases').find('tbody')
        for row in table.find_all('tr'):
            version = next(row.find('a').stripped_strings)
            released = row.find('time').attrs['datetime']
            yield Release(self, version, released)


@click.group(name='releases', cls=DefaultGroup, default='all')
@click.argument('project')
@click.pass_context
def releases_cli(ctx, project):
    """
    """
    session = ctx.obj['session']
    ctx.obj['releases'] = Releases(session, project)


@releases_cli.command('all')
@click.pass_context
def all_releases(ctx, **kwargs):
    rows = [[release.version, release.released]
            for release in ctx.obj['releases'].all()]
    click.echo(str(Table(['Version', 'Released'], rows)))
