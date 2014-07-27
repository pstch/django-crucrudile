Installation
============

.. contents::

At this time, the only requirements to run ``django-crucrudile`` are
**Python** (3.3, 3.4), and **Django** (1.6). Django will be installed
automatically if needed.

*Note* : backporting for Python 2.6 or could be done easily, ping me if you need it.

From Python package index
-------------------------

To install from PyPI ::

  pip install django-crucrudile

(This installs the latest release in
https://pypi.python.org/pypi/django-crucrudile/ )

From Git tags
-------------

To install from Git master branch ::

  pip install -e git+https://github.com/pstch/django-crucrudile.git@master#egg=django-crucrudile

(This installs the latest release (major, minor or patch) in the
master branch, use ``@develop`` to install development version. You
can also use ``@tag``, replacing tag by a release name (ex: 'v1.4.1')
(Git tag, see Releases tab in GitHub).

To install from Git develop branch ::

  pip install -e git+https://github.com/pstch/django-crucrudile.git@develop#egg=django-crucrudile

From source
-----------

To install from source ::

  git clone https://github.com/pstch/django-crucrudile.git
  cd django-crucrudile
  python setup.py install

If you want the development version (default branch is ``master``,
containing latest release), run ``git checkout develop`` before
``python setup.py install``


``django-crucrudile`` is a Python package, and it does **not** need to
be included as an application (in ``INSTALLED_APPS``) in Django. You
only need to import the needed modules in your Python files.
