import configparser
import json
import os
from json import JSONDecodeError
from typing import Union, Tuple

import keyring
from bs4 import BeautifulSoup
from keyring.errors import KeyringError
from requests import Session, Response
from requests.cookies import RequestsCookieJar

from pypi_admin.exceptions import PypiTwoFactorRequired, PypiKeyringError

URL = 'https://pypi.org/'
KEYRING_SESSION_NAME = 'pypi-client-session'


def get_config(path: str = "~/.pypirc"):
    path = os.path.expanduser(path)
    parser = configparser.RawConfigParser()
    if os.path.isfile(path):
        parser.read(path)
        return parser


def get_pypirc_login(path: str = "~/.pypirc") -> Union[Tuple[None, None], Tuple[str, str]]:
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
        self._two_factor_soup = None

    def is_authenticated(self):
        response = self.request('/manage/account/', options=dict(allow_redirects=False))
        return not response.is_redirect

    def login(self):
        response = self.form_request('/account/login/', data={
            'username': self.username,
            'password': self.password,
        })
        soup = BeautifulSoup(response.text, 'html.parser')
        twofa = soup.find('div', class_='twofa-login__method')
        if twofa:
            self._two_factor_soup = twofa
            raise PypiTwoFactorRequired

    def two_factor(self, value):
        assert self._two_factor_soup is not None, "Login before use two factor"
        url = self._two_factor_soup.find('form').attrs['action']
        self._form_request(url, self._two_factor_soup, {
            'method': 'totp',
            'totp_value': value,
        })

    def request(self, path: str, method: str = 'get', data=None, validate=True,
                options=None) -> Response:
        options = options or {}
        url = '{}/{}'.format(URL.rstrip('/'), path.lstrip('/'))
        headers = {
            'Referer': self.referrer
        }
        self.referrer = url
        response = self.session.request(method, url, data=data, headers=headers, **options)
        if validate:
            response.raise_for_status()
        return response

    def form_request(self, path: str, data: dict = None,
                     original_path: Union[str, None] = None) -> Response:
        data = dict(data or {})
        original_path = original_path or path
        soup = self.soup_request(original_path)
        return self._form_request(path, soup, data)

    def _form_request(self, path, html_or_soup, data):
        if isinstance(html_or_soup, (str, bytes)):
            soup = BeautifulSoup(html_or_soup, 'html.parser')
        else:
            soup = html_or_soup
        csrf_token = soup.find('input', attrs={"name": "csrf_token"}).attrs['value']
        data['csrf_token'] = csrf_token
        return self.request(path, data=data, method='post')

    def soup_request(self, path: str, **kwargs) -> BeautifulSoup:
        response = self.request(path, **kwargs)
        return BeautifulSoup(response.text, 'html.parser')

    def save_session(self):
        cookies = dict(self.session.cookies)
        try:
            keyring.set_password(KEYRING_SESSION_NAME, self.username, json.dumps(cookies))
        except KeyringError as e:
            raise PypiKeyringError(f'{e}')

    def restore_session(self):
        cookies = RequestsCookieJar()
        try:
            data = keyring.get_password(KEYRING_SESSION_NAME, self.username)
            if data is None:
                # Session is not saved
                return
            data = json.loads(data)
        except (KeyringError, JSONDecodeError) as e:
            raise PypiKeyringError(f'{e}')
        cookies.update(data)
        self.session.cookies = cookies


if __name__ == '__main__':
    get_config()
