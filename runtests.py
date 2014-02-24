#!/usr/bin/env python
#pylint: disable=W0142,C0111
"""
#TODO: Missing module docstring
"""
import sys

from django.conf import settings
from django.core.management import execute_from_command_line

if not settings.configured:
    SETTINGS_DICT = {}
    # Database settings
    SETTINGS_DICT.update({
        'DATABASES' : {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }}
    })
    # INSTALLED_APPS
    SETTINGS_DICT.update({
        'INSTALLED_APPS' : (
            'django_pstch_helpers',
            'tests',
        )
    })

    # django-markitup args
    SETTINGS_DICT.update({
        'MARKITUP_FILTER' : ('markdown.markdown', {'safe_mode': True})
    })

    # Misc
    SETTINGS_DICT.update({
        'ROOT_URLCONF' : None,
        'USE_TZ' : True,
        'SECRET_KEY' : 'so long and thanks for all the fish'
    })

    settings.configure(**SETTINGS_DICT)


def runtests():
    argv = sys.argv[:1] + sys.argv[1:]
    execute_from_command_line(argv)
    sys.exit(0)


if __name__ == '__main__':
    runtests()
