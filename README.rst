cdrouter
========

Simple wrapper for the CDRouter Web
API. https://support.qacafe.com/cdrouter-web-api/

For more information on CDRouter, please visit http://www.qacafe.com/.

Installing
==========

cdrouter is available on PyPI.

.. code-block:: bash

    $ pip install cdrouter


Usage
=====

.. code-block:: python

    import cdrouter

    service = cdrouter.Service('http://localhost:8015', token='deadbeef')

    print service.packages().list(filters=['name~'], page=2).json()
    print service.packages().get(164).json()
