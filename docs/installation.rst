.. highlight:: console

============
Installation
============


Stable release
--------------

To install pypi-client, run this command in your terminal:

.. code-block:: console

    $ pip install pypi_admin

This is the preferred method to install pypi-client, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Other releases
--------------
You can install other versions from Pypi using::

    $ pip install pypi-client==<version>

For versions that are not in Pypi (it is a development version)::

    $ pip install git+https://github.com/Nekmo/pypi-client@<branch>#egg=pypi-client




From sources
------------

The sources for pypi-client can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/Nekmo/pypi-client

Or download the `tarball`_:

.. code-block:: console

    $ curl -OL https://github.com/Nekmo/pypi-client/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/Nekmo/pypi-client
.. _tarball: https://github.com/Nekmo/pypi-client/tarball/master
