import click
from click_default_group import DefaultGroup

from pypi_admin.table import Table


class Event:
    def __init__(self, events: 'Events', action: str, username: str,
                 datetime, ip_address):
        self.events = events
        self.action = action
        self.username = username
        self.datetime = datetime
        self.ip_address = ip_address


class Events:
    def __init__(self, session, project):
        self.session = session
        self.project = project

    def all(self):
        soup = self.session.soup_request(f'/manage/project/{self.project}/history/')
        table = soup.find('table', class_='table--security-logs').find('tbody')
        for row in table.find_all('tr'):
            action = next(row.find('strong').stripped_strings)
            username = row.find('small').find('a').text
            datetime = row.find('time').attrs['datetime']
            ip_address = list(row.find_all('td')[2].stripped_strings)[1]
            yield Event(self, action, username, datetime, ip_address)


@click.group(name='events', cls=DefaultGroup, default='all')
@click.argument('project')
@click.pass_context
def events_cli(ctx, project):
    """
    """
    session = ctx.obj['session']
    ctx.obj['events'] = Events(session, project)


@events_cli.command('all')
@click.pass_context
def all_events(ctx, **kwargs):
    rows = [[event.action, event.username, event.datetime, event.ip_address]
            for event in ctx.obj['events'].all()]
    click.echo(str(Table(['Action', 'Username', 'Datetime', 'IP Address'], rows)))
