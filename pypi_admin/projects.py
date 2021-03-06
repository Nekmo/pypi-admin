import click
from click_default_group import DefaultGroup

from pypi_admin.table import Table


class Project:
    def __init__(self, projects: 'Projects', title, description, last_released):
        self.projects = projects
        self.title = title
        self.description = description
        self.last_released = last_released


class Projects:
    def __init__(self, session):
        self.session = session

    def all(self):
        soup = self.session.soup_request('/manage/projects/')
        for project in soup.find_all('div', class_='package-snippet'):
            title = next(project.find('h3', class_='package-snippet__title').stripped_strings)
            description = next(project.find('p', class_='package-snippet__description').stripped_strings)
            last_released = project.find('time').attrs['datetime']
            yield Project(
                self, title, description, last_released
            )


@click.group(name='projects', cls=DefaultGroup, default='all', default_if_no_args=True)
@click.pass_context
def projects_cli(ctx):
    """
    """
    session = ctx.obj['session']
    ctx.obj['projects'] = Projects(session)


@projects_cli.command('all')
@click.pass_context
def all_projects(ctx, **kwargs):
    rows = [[token.title, token.description, token.last_released]
            for token in ctx.obj['projects'].all()]
    click.echo(str(Table(['Title', 'Description', 'Last released'], rows)))
