Introduction
============

cdrouter is a simple Python wrapper for the CDRouter Web
API. https://support.qacafe.com/cdrouter/cdrouter-web-api/

For more information on CDRouter, please visit http://www.qacafe.com/.

Install/Upgrade
---------------

cdrouter is available on PyPI_.  To install the latest stable version from PyPI:

.. _PyPI: https://pypi.python.org/pypi/cdrouter

.. code-block:: bash

    $ pip install -U cdrouter

cdrouter supports Python 3.5 or newer.

Usage
-----

First create a :class:`CDRouter <cdrouter.CDRouter>` object, passing
it the URL of your CDRouter system, for example ``http://localhost``,
``https://cdrouter.example.com`` or ``http://172.20.0.1:8015``.  If
your CDRouter system uses a self-signed certificate for HTTPS
connections (the default), you will need to pass in ``insecure=True``
to disable certificate validation.  If Automatic Login is not enabled
on your CDRouter system, you will need to provide authentication
credentials by passing in an API token via the ``token`` parameter or
a username and password via the ``username`` and ``password``
parameters.  If ``token`` is not specified, it will default to the
value of the ``CDROUTER_API_TOKEN`` environment variable.
:class:`CDRouter <cdrouter.CDRouter>` will prompt for a username and
password as necessary if Automatic Login is not enabled and an API
token is not provided.

.. code-block:: python

    import time

    from cdrouter import CDRouter
    from cdrouter.cdrouter import CDRouterError
    from cdrouter.filters import Field as field
    from cdrouter.jobs import Job
    from cdrouter.jobs import Options

    c = CDRouter('http://localhost', token='deadbeef')

    for p in c.packages.iter_list(filter=field('tags').contains('noretry')):
        print('Launching package {}'.format(p.name))

        try:
            j = c.jobs.launch(Job(package_id=p.id, options=Options(extra_cli_args='-testvar myvar=example')))
        except CDRouterError as ce:
            print('Error launching job: {}'.format(ce))
            continue

        while j.result_id == None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        print('    Result-ID: {}'.format(j.result_id))

    print('done.')

More examples of using cdrouter can be found here_.  Please see the
:ref:`Reference <reference>` page for more information on available
fields and methods for each class.

.. _here: https://github.com/qacafe/cdrouter.py/tree/master/examples


