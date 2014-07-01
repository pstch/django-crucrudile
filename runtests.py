#!/usr/bin/env python
# pylint: disable=W0142,C0111
"""
#TODO: Missing module docstring
"""
import sys
import os

from django.core.management import execute_from_command_line


def run_django_tests():
    print("#### Running tests using Django test runner...")
    print("#### (Disable with NO_DJANGO_TESTS=1)")
    argv = ['runtests.py', 'test'] + sys.argv[1:]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    execute_from_command_line(argv)
    print("#### Done running tests with Django test runner.")


def run_sphinx_tests():
    print("#### Running tests using Sphinx doctest builder...")
    print("#### (Disable with NO_SPHINX_TESTS=1)")
    os.system("sphinx-build -E -c docs -b doctest -a docs doctests")
    print("#### Done running tests using Sphinx doctest builder.")


def runtests():
    if os.environ.get('NO_DJANGO_TESTS') != '1':
        run_django_tests()
    if os.environ.get('NO_SPHINX_TESTS') != '1':
        run_sphinx_tests()

if __name__ == '__main__':
    runtests()
