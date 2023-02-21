cdrouter
========

.. image:: https://img.shields.io/pypi/v/cdrouter.svg
    :target: https://pypi.python.org/pypi/cdrouter

Simple Python wrapper for the CDRouter Web
API. https://support.qacafe.com/cdrouter/cdrouter-web-api/

For more information on CDRouter, please visit http://www.qacafe.com/.

Installing/Upgrading
====================

cdrouter is available on PyPI.  To install the latest stable version from PyPI:

.. code-block:: bash

    $ pip install -U cdrouter

cdrouter supports Python 3.5 or newer.

Documentation
=============

See http://cdrouterpy.readthedocs.io/.

Unit Tests
==========

Unit tests for cdrouter.py are written using pytest
(https://docs.pytest.org) and run with tox (https://tox.wiki).  Each
test starts up an ephemeral CDRouter Docker container to test against.
Tests are stored in the ``tests/`` directory.  The following tooling
is required to run the unit tests:

- Docker must be installed and the ``docker`` command runnable by the
  current user.  Follow the official install instructions
  (https://docs.docker.com/engine/install/) to ensure this is the
  case.

- Python 3.8 must be installed with a ``python3.8`` binary available
  in your ``PATH``.

- ``tox`` must be installed via ``pip3``:

  .. code-block:: bash

      $ pip3 install -U tox

  If you do not already have ``pip3`` installed, follow the official
  install instructions (https://pip.pypa.io/en/stable/installation/)
  or use the ``get-pip.py`` script below to perform the installation
  automatically:

  .. code-block:: bash

      $ curl -s https://bootstrap.pypa.io/pip/get-pip.py | python3

The unit tests are controlled by a number of a environment variables,
some required while others are optional.  Optional environment
variables are listed further below.  The required environment
variables are:

- ``CDR_DOCKER_IMAGE``: The CDRouter Docker image to use to test
  against.  The unit tests automatically create and teardown Docker
  containers running this image during testing.  Its value should be a
  Docker image name that can be passed directly to ``docker run``.  A
  good default is:

  .. code-block:: bash

      CDR_DOCKER_IMAGE=registry.gitlab.com/qacafe/cdrouter/cdrouter/cdrouter:latest

  which should always be the latest CDRouter release.

- ``CDR_DOCKER_LICENSE``: The base64-encoded contents of a CDRouter
  license file with all addons enabled to be used in the CDRouter
  Docker containers which are created during testing.  If the CDRouter
  license file to be used exists at ``/path/to/cdrouter.lic``, set
  this variable to:

  .. code-block:: bash

      CDR_DOCKER_LICENSE=$(base64 -w0 /path/to/cdrouter.lic)

Finally, run the unit tests via:

.. code-block:: bash

    $ CDR_DOCKER_IMAGE=registry.gitlab.com/qacafe/cdrouter/cdrouter/cdrouter:latest \
      CDR_DOCKER_LICENSE=$(base64 -w0 /path/to/cdrouter.lic) \
      tox -p

This will both lint the codebase using ``pylint`` and run all unit
tests.  You may sometimes want to run only a subset of tests.  To run
just the tests in ``tests/test_configs.py``, run:

.. code-block:: bash

    $ CDR_DOCKER_IMAGE=registry.gitlab.com/qacafe/cdrouter/cdrouter/cdrouter:latest \
      CDR_DOCKER_LICENSE=$(base64 -w0 /path/to/cdrouter.lic) \
      tox -e py38 -- tests/test_configs.py

To run just the ``test_list`` test in the ``TestConfigs`` class of
``tests/test_configs.py``, run:

.. code-block:: bash

    $ CDR_DOCKER_IMAGE=registry.gitlab.com/qacafe/cdrouter/cdrouter/cdrouter:latest \
      CDR_DOCKER_LICENSE=$(base64 -w0 /path/to/cdrouter.lic) \
      tox -e py38 -- tests/test_configs.py::TestConfigs::test_list

Below are the optional environment variables used by the unit tests:

- ``CDR_DOCKER_PULL``: By default, the unit tests will ensure the
  Docker image specified by ``CDR_DOCKER_IMAGE`` is present and up to
  date via a call to ``docker pull``.  Sometimes this isn't necessary
  or desired, in which case setting ``CDR_DOCKER_PULL=0`` will cause
  the unit tests to skip this step and assume the Docker image is
  already present and up to date.  Setting ``CDR_DOCKER_PULL=0`` is
  often necessary if ``CDR_DOCKER_IMAGE`` is set to a locally-built
  image rather than one pulled down from a Docker registry.

- ``CLOUDSHARK_URL`` & ``CLOUDSHARK_TOKEN``: These variables specify
  the URL and valid API token of a CloudShark appliance.  If these are
  not set, tests which require uploading capture files to a CloudShark
  appliance are skipped.

- ``RUN_LOUNGE_TESTS``, ``LOUNGE_EMAIL``, ``LOUNGE_URL`` &
  ``LOUNGE_INSECURE``: By default, tests which require communicating
  with the QA Cafe Lounge are skipped.  These tests can be run by
  setting ``RUN_LOUNGE_TESTS=1``, in which case ``LOUNGE_EMAIL`` must
  be set to a valid email address for a contact in same Lounge account
  as the CDRouter license stored in ``CDR_DOCKER_LICENSE``.
  Additionally, ``LOUNGE_URL`` and ``LOUNGE_INSECURE`` can be used to
  have the tests talk to a non-production Lounge.
