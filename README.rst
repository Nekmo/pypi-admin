.. image:: https://raw.githubusercontent.com/Nekmo/pypi-manage/master/logo.png
    :width: 100%

|

.. image:: https://img.shields.io/travis/Nekmo/pypi-manage.svg?style=flat-square&maxAge=2592000
  :target: https://travis-ci.org/Nekmo/pypi-manage
  :alt: Latest Travis CI build status

.. image:: https://img.shields.io/pypi/v/pypi-manage.svg?style=flat-square
  :target: https://pypi.org/project/pypi-manage/
  :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pypi-manage.svg?style=flat-square
  :target: https://pypi.org/project/pypi-manage/
  :alt: Python versions

.. image:: https://img.shields.io/codeclimate/github/Nekmo/pypi-manage.svg?style=flat-square
  :target: https://codeclimate.com/github/Nekmo/pypi-manage
  :alt: Code Climate

.. image:: https://img.shields.io/codecov/c/github/Nekmo/pypi-manage/master.svg?style=flat-square
  :target: https://codecov.io/github/Nekmo/pypi-manage
  :alt: Test coverage

.. image:: https://img.shields.io/requires/github/Nekmo/pypi-manage.svg?style=flat-square
     :target: https://requires.io/github/Nekmo/pypi-manage/requirements/?branch=master
     :alt: Requirements Status


###########
pypi-manage
###########

Manage your Pypi warehouse account from console or using a awesome Python API. For example use the command line to
create an upload token for an app:

.. code-block:: shell

    $ pypi-manage tokens create "Token name" my-project

Use this command with other programs. For example you can use it together with Travis:

.. code-block:: shell

    $ travis encrypt $(pypi-manage tokens create "Token name" my-project)

Create a token from Python:

.. code-block:: python

    from pypi_admin.session import PypiSession, get_pypirc_login
    from pypi_admin.manage import PypiClient
    from pypi_admin.exceptions import PypiTwoFactorRequired

    session = PypiSession(*get_pypirc_login())  # get username/password from pypirc
    # Optional: use session.restore_session() instead session.login()
    try:
        session.login()
    except PypiTwoFactorRequired:
        session.two_factor(input('Insert TOTP: '))
    # Optional: use session.save_session()

    manage = PypiClient(session)
    token = manage.tokens.create('Token name', 'my-project')
    print(f'{token.token_id}: {token.token}')


To install pypi-manage, run this command in your terminal:

.. code-block:: console

    $ python -m pip -U install pypi-manage

This is the preferred method to install pypi-manage, as it will always install the most recent stable release.


Current features
================

* List, create or delete **tokens**. Get help using ``pypi-manage tokens --help``.
* List project **collaborators**.  Use ``pypi-manage collaborators <project name> all``.
* List project **history** (events).  Use ``pypi-manage events <project name> all``.
* List project **releases**.  Use ``pypi-manage releases <project name> all``.
* List **projects**.  Use ``pypi-manage projects``.

