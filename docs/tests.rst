Running the tests
=================

.. contents::

.. note:: If you are using a virtual environment, it should be activated before running the following code blocks.

- `Online tests <https://travis-ci.org/pstch/django-crucrudile/builds>`_ (Travis-CI)
- `Online coverage reports <https://coveralls.io/r/pstch/django-crucrudile>`_ (Coveralls)

Dependencies
------------

Dependencies (and test dependencies) are set in the ``setup.py``, and
installed when the package gets installed (or when the tests are
executed for test dependencies).

Running tests using ``setuptools``
----------------------------------

The test collector used in ``setup.py`` is the ``runtests.py`` script
uses the nose test runner to run tests.

.. warning:: Documentation tests are collected as a single unit test !

- nose tests can be disabled using ``NO_NOSE_TESTS=1``
- doctests can be disabled using ``NO_SPHINX_TESTS=1``.

.. note::

   The following command does not need any dependency to be installed
   beforehand, as they will be installed (as Python eggs, in the
   working directory) by ``setuptools`` automatically. However, you
   may want to install them yourself before running the tests (to
   avoid polluting your working directory with the Python eggs built
   by ``setuptools``) by using ``pip``, in that case use ``pip
   install -r tests/requirements.txt``.

.. code-block:: sh

   python setup.py test

Running tests manually
----------------------

.. warning::

   To run the tests manually, needed dependencies (``pip install -r
   tests/requirements.txt``) have to be available in the environment.

.. warning::

   To run the tests manually, the ``DJANGO_SETTINGS_MODULE``
   environment variable must be set to ``tests.settings``, or to a
   valid settings module. (``export
   DJANGO_SETTINGS_MODULE=tests.settings``)

Nose tests
~~~~~~~~~~

To run nosetests (they include the doctests), use :

.. code-block:: sh

   nosetests

Documentation tests
~~~~~~~~~~~~~~~~~~~

To run doctests manually, use :

.. code-block:: sh

   sphinx-build -E -c docs -b html -a docs var/docs_doctests

Code coverage
-------------

Coverage report is automatically executed while running nose tests. ``nosetests`` prints a basic coverage report, and the HTML coverage report is generated in ``vars/coverage_html``.

Coverage reports can also be seen at `coveralls.io/r/pstch/django-crucrudile <https://coveralls.io/r/pstch/django-crucrudile>`_.

Call graphs
-----------

If you install pycallgraph (``pip install pycallgraph``), you can use it to trace call graphs of the executed code. Sadly, it does not work with nosetests, but it's very easy to use it manually, for specific tests :

.. code-block:: sh

   echo "
   import tests.integration.test_routers as tests
   case = tests.RouterTestCase()
   case.setUp()
   case.test_get_str_tree()
   " | pycallgraph -I django_crucrudile\* graphviz -- /dev/stdin

The call graph will be written to ``pycallgraph.png``.

.. warning::

   ``pycallgraph`` may need GraphViz and pydot to be installed (a Python 3
   compatible version. At this date, it is available in
   `bitbucket.org/prologic/pydot <https://bitbucket.org/prologic/pydot>`_.)
