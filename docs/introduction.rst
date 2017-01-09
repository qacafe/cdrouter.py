Introduction
============

cdrouter is a simple Python wrapper for the CDRouter Web
API. https://support.qacafe.com/cdrouter-web-api/

For more information on CDRouter, please visit http://www.qacafe.com/.

Download & Install
------------------

cdrouter is available on PyPI.

.. code-block:: bash

    $ pip install cdrouter


Usage
-----

.. code-block:: python

    import cdrouter

    s = cdrouter.Service('http://localhost:8015', token='deadbeef')
    
    for p in s.packages.list(filter=['tags@>{demo}'], limit='none').json()['data']:
        print 'Launching package ' + p['name']

        resp = s.jobs.launch({'package_id': p['id'], 'extra_cli_args': '-testvar myvar=example'})
        job_id = resp.json()['data']['id']

        result_id = '0'
        while result_id == '0':
            resp = s.jobs.get(job_id)
            if 'result_id' in resp.json()['data']:
                result_id = resp.json()['data']['result_id']
            time.sleep(1)

        print '    Result-ID: ' + result_id

    print 'done.'
