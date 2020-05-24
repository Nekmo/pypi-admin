from pypi_client.session import PypiSession
from pypi_client.tokens import Tokens


class PypiClient:
    def __init__(self, session: PypiSession):
        self.session = session

    @property
    def tokens(self):
        return Tokens(self.session)
