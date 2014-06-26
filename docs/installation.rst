Installation
============

At this time, the only requirements to run ``django-crucrudile`` are **Python** (3.3), and **Django** (1.6).

*Note* : support for Python 2.6 or 2.6 can be added pretty easily, ping me if you need it.

As ``django-crucrudile`` is still in the initial development phase, I did not yet upload it to the Python package index. To install it, you can either install it as a Python egg with ``pip``, or download the source and run ``setup.py install``.

To install with ``pip``::

  pip install -e git+https://github.com/pstch/django-crucrudile.git@master#egg=django-crucrudile

(This installs the latest release (major, minor or patch), use `@develop` to install development version. You can also use `@tag`, replacing tag by a release name (ex: 'v1.4.1') (Git tag, see Releases tab in GitHub).

To install from source ::

  git clone https://github.com/pstch/django-crucrudile.git
  cd django-crucrudile
  python setup.py install

If you want the development version (default branch is `master`, containing latest release), run `git checkout develop` before `python setup.py install`


``django-crucrudile`` is a Python package, and it does **not** need to be included as an application (in ``INSTALLED_APPS``) in Django. You only need to import the needed modules in your Python files.
