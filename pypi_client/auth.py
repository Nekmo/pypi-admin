import os

from bs4 import BeautifulSoup
from requests import Session


class Auth:
    def __init__(self):
        username, password = os.environ.get('USERNAME'), os.environ.get('PASSWORD')
        self.session = Session()
        self.session.auth = (username, password)
        r = self.session.get('https://pypi.org/account/login/', headers={
            'Referer': 'https://pypi.org/'
        })
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf_token = soup.find('input', attrs={"name": "csrf_token"}).attrs['value']
        r = self.session.post('https://pypi.org/account/login/', {
            'username': username,
            'password': password,
            'csrf_token': csrf_token,
        }, headers={'Referer': 'https://pypi.org/account/login/'})
        r.raise_for_status()
        r = self.session.get('https://pypi.org/manage/account/')
        pass


if __name__ == '__main__':
    Auth()
