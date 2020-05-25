###########
pypi-client
###########


.. image:: https://img.shields.io/travis/Nekmo/pypi-client.svg?style=flat-square&maxAge=2592000
  :target: https://travis-ci.org/Nekmo/pypi-client
  :alt: Latest Travis CI build status

.. image:: https://img.shields.io/pypi/v/pypi-client.svg?style=flat-square
  :target: https://pypi.org/project/pypi-client/
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pypi-client.svg?style=flat-square
  :target: https://pypi.org/project/pypi-client/
  :alt: Python versions

.. image:: https://img.shields.io/codeclimate/github/Nekmo/pypi-client.svg?style=flat-square
  :target: https://codeclimate.com/github/Nekmo/pypi-client
  :alt: Code Climate

.. image:: https://img.shields.io/codecov/c/github/Nekmo/pypi-client/master.svg?style=flat-square
  :target: https://codecov.io/github/Nekmo/pypi-client
  :alt: Test coverage

.. image:: https://img.shields.io/requires/github/Nekmo/pypi-client.svg?style=flat-square
     :target: https://requires.io/github/Nekmo/pypi-client/requirements/?branch=master
     :alt: Requirements Status


Manage your Pypi warehouse account from console or using a awesome Python API. For example use the command line to
create an upload token for an app:

.. code-block:: shell

    $ pypi-client tokens create "Token name" my-project

Use this command with other programs. For example you can use it together with Travis:

.. code-block:: shell

    $ travis encrypt $(pypi-client tokens create "Token name" my-project)

Create a token from Python:

.. code-block:: python

    from pypi_client.session import PypiSession, get_pypirc_login
    from pypi_client.client import PypiClient
    from pypi_client.exceptions import PypiTwoFactorRequired

    session = PypiSession(*get_pypirc_login())  # get username/password from pypirc
    # Optional: use session.restore_session() instead session.login()
    try:
        session.login()
    except PypiTwoFactorRequired:
        session.two_factor(input('Insert TOTP: '))
    # Optional: use session.save_session()

    client = PypiClient(session)
    token = client.tokens.create('Token name', 'my-project')
    print(f'{token.token_id}: {token.token}')


To install pypi-client, run this command in your terminal:

.. code-block:: console

    $ sudo pip install pypi-client

This is the preferred method to install pypi-client, as it will always install the most recent stable release.


Features
========

* TODO

