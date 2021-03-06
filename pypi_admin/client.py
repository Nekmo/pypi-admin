from pypi_admin.session import PypiSession
from pypi_admin.tokens import Tokens


class PypiClient:
    def __init__(self, session: PypiSession):
        self.session = session

    @property
    def tokens(self):
        return Tokens(self.session)
