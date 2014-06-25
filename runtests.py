#!/usr/bin/env python
#pylint: disable=W0142,C0111
"""
#TODO: Missing module docstring
"""
import sys
import os

from django.core.management import execute_from_command_line

def runtests():
    argv = ['runtests.py', 'test'] + sys.argv[1:]
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    execute_from_command_line(argv)
    sys.exit(0)


if __name__ == '__main__':
    runtests()

