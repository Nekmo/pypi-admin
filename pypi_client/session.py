import configparser
import os
from typing import Union, Tuple

from bs4 import BeautifulSoup
from requests import Session, Response

URL = 'https://pypi.org/'


def get_config(path: str = "~/.pypirc"):
    path = os.path.expanduser(path)
    parser = configparser.RawConfigParser()
    if os.path.isfile(path):
        parser.read(path)
        return parser


def get_pypi_login(path: str = "~/.pypirc") -> Union[Tuple[None, None], Tuple[str, str]]:
    config = get_config(path)
    if config is None:
        return None, None
    for section_name in ['server-login', 'pypi']:
        if config.has_option(section_name, "username") and \
                config.has_option(section_name, "password"):
            section = config[section_name]
            return section['username'], section['password']
    return None, None


class PypiSession:
    def __init__(self, username: str, password: str):
        self.username, self.password = username, password
        self.session = Session()
        self.referrer = URL

    def login(self):
        self.form_request('/account/login/', data={
            'username': self.username,
            'password': self.password,
        })

    def request(self, path: str, method: str = 'get', data=None, validate=True) -> Response:
        url = '{}/{}'.format(URL.rstrip('/'), path.lstrip('/'))
        headers = {
            'Referer': self.referrer
        }
        self.referrer = url
        response = self.session.request(method, url, data=data, headers=headers)
        if validate:
            response.raise_for_status()
        return response

    def form_request(self, path: str, data: dict = None,
                     original_path: Union[str, None] = None) -> Response:
        data = dict(data or {})
        original_path = original_path or path
        soup = self.soup_request(original_path)
        csrf_token = soup.find('input', attrs={"name": "csrf_token"}).attrs['value']
        data['csrf_token'] = csrf_token
        return self.request(path, data=data, method='post')

    def soup_request(self, path: str, **kwargs) -> BeautifulSoup:
        response = self.request(path, **kwargs)
        return BeautifulSoup(response.text, 'html.parser')

if __name__ == '__main__':
    get_config()
