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

Running tests
----------------------

The test register used in ``setup.py`` is the ``runtests.py`` script
uses the nose test runner and Sphinx to run tests.nose tests can be
disabled using ``NO_NOSE_TESTS=1``, and doctests can be disabled using
``NO_SPHINX_TESTS=1``.

.. code-block:: sh

   python setup.py test

Nose tests
~~~~~~~~~~

The ``nosetests`` command can also be used to run the tests (doctests will not be included, and test dependencies not installed).

Documentation tests
~~~~~~~~~~~~~~~~~~~

To run doctests, use :

.. code-block:: sh

   sphinx-build -E -c docs -b html -a docs var/docs_doctests

Code coverage
-------------

.. warning:: The code coverage report does not cover documentation tests.

Coverage report is automatically executed while running nose tests. ``nosetests`` prints a basic coverage report, and the HTML coverage report is generated in ``vars/coverage_html``. Coverage reports can also be seen at `coveralls.io/r/pstch/django-crucrudile <https://coveralls.io/r/pstch/django-crucrudile>`_.

Call graphs
-----------

If you install pycallgraph (``pip install pycallgraph``), you can use it to trace call graphs of the executed code. Sadly, it does not work with nosetests, but it's very easy to use it manually, for specific tests :

.. code-block:: sh

   echo "
   import django_crucrudile.tests.integration.tests_routers as tests
   case = tests.RouterTestCase()
   case.setUp()
   case.test_get_str_tree()
   " | pycallgraph -I django_crucrudile\* graphviz -- /dev/stdin

The call graph will be written to ``pycallgraph.png``.

.. warning::

   ``pycallgraph`` may need ``pydot`` to be installed (a Python 3
   compatible version. At this date, it is available in
   `bitbucket.org/prologic/pydot <https://bitbucket.org/prologic/pydot>`_.)
