Introduction
============

cdrouter is a simple Python wrapper for the CDRouter Web
API. https://support.qacafe.com/cdrouter-web-api/

For more information on CDRouter, please visit http://www.qacafe.com/.

Download & Install
------------------

cdrouter is available on PyPI_.

.. _PyPI: https://pypi.python.org/pypi/cdrouter

.. code-block:: bash

    $ pip install -U cdrouter


Usage
-----

First create a :class:`CDRouter <cdrouter.CDRouter>` object, passing
it the URL of your CDRouter system.  The ``token`` parameter should be
set to a valid API token on your CDRouter system.  If ``token`` is not
specified, it will default to the value of the ``CDROUTER_API_TOKEN``
environment variable.  The ``token`` argument can be omitted for
CDRouter systems where Automatic Login is enabled.

.. code-block:: python

    import time
    from cdrouter import CDRouter
    from cdrouter.cdrouter import CDRouterError
    from cdrouter.filters import Field as field
    from cdrouter.jobs import Job

    c = CDRouter('http://localhost:8015', token='deadbeef')

    for p in c.packages.iter_list(filter=field('tags').contains('noretry')):
        print('Launching package ' + p.name)

        try:
            j = c.jobs.launch(Job(package_id=p.id, extra_cli_args='-testvar myvar=example'))
        except CDRouterError as ce:
            print('Error launching job: {}'.format(ce))

        while j.result_id == None:
            time.sleep(1)
            j = c.jobs.get(j.id)

        print('    Result-ID: ' + j.result_id)

    print('done.')

More examples of using cdrouter can be found here_.  Please see the
:ref:`Reference <reference>` page for more information on available
fields and methods for each class.

.. _here: https://github.com/qacafe/cdrouter.py/tree/master/examples


