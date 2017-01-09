Introduction
============

cdrouter is a simple wrapper for the CDRouter Web
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

    service = cdrouter.Service('http://localhost:8015', token='deadbeef')
    packages = cdrouter.PackagesService(service)

    print packages.list(filter=['name~'], page=2).json()
    print packages.get(164).json()
