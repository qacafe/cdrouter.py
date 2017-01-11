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

.. code-block:: python

    import time
    import cdrouter
    from cdrouter.jobs import Job

    cdr = cdrouter.Service('http://localhost:8015', token='deadbeef')

    for p in cdr.packages.list(filter=['tags@>{noretry}'], limit='none'):
        print 'Launching package ' + p.name

        j = cdr.jobs.launch(Job(package_id=p.id, extra_cli_args='-testvar myvar=example'))

        while j.result_id == None:
            time.sleep(1)
            j = cdr.jobs.get(j.id)

        print '    Result-ID: ' + j.result_id

    print 'done.'
