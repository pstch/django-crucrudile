Running the tests
=================

.. _Online tests: https://travis-ci.org/pstch/django-crucrudile/builds
.. _Online coverage reports: https://coveralls.io/r/pstch/django-crucrudile

.. note:: If you are using a virtual environment, it should be activated before running the following code blocks.

Dependencies
------------

Dependencies are stored in the ``requirements.txt`` file. Tests need another set of dependencies stored in ``tests/requirements.txt``.

.. code-block:: sh

   pip install -r requirements.txt
   pip install -r tests/requirements.txt


``runtests.py`` script
----------------------

The ``runtests.py`` script uses the nose test runner and Sphinx to run
tests.nose tests can be disabled using ``NO_NOSE_TESTS=1``, and
doctests can be disabled using ``NO_SPHINX_TESTS=1``.

.. code-block:: sh

   ./runtests.py

Nose tests
~~~~~~~~~~

The ``nosetests`` command can also be used to run the tests (doctests will not be included).

Documentation tests
~~~~~~~~~~~~~~~~~~~

To run doctests, use :

.. code-block:: sh

   sphinx-build -E -c docs -b html -a docs var/docs_doctests

Code coverage
-------------

.. warning:: The code coverage report does not cover documentation tests.

Coverage report is automatically executed while running nose tests. ``nosetests`` prints a basic coverage report, and the HTML coverage report is generated in ``vars/coverage_html``. Coverage reports can also be seen at .. _coveralls.io/r/pstch/django-crucrudile: https://coveralls.io/r/pstch/django-crucrudile .

Call graphs
-----------

If you install pycallgraph (``pip install pycallgraph``, may require some additional dependencies), you can use it to trace call graphs of the executed code. Sadly, it does not work with nosetests, but it's very easy to use it manually, for specific tests :

.. code-block:: sh

   echo "
   import django_crucrudile.tests.integration.tests_routers as tests
   case = tests.RouterTestCase()
   case.setUp()
   case.test_get_str_tree()
   " | pycallgraph -I django_crucrudile\* graphviz -- /dev/stdin

The call graph will be written to ``pycallgraph.png``.
