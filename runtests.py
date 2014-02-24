#!/usr/bin/env python
import sys

from django import VERSION

from django.conf import settings
from django.core.management import execute_from_command_line

if not settings.configured:
    args = {}
    # Database settings
    args.update({
        'DATABASES' : {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }}
    })
    # INSTALLED_APPS
    args.update({
        'INSTALLED_APPS' : (
            'django_pstch_helpers',
            'tests',
        )
    })

    # django-markitup args
    args.update({
        'MARKITUP_FILTER' : ('markdown.markdown', {'safe_mode': True})
    })

    # Misc args
    args.update({
        'ROOT_URLCONF' : None,
        'USE_TZ' : True,
        'SECRET_KEY' : 'so long and thanks for all the fish'
    })

    settings.configure(**args)


def runtests():
    argv = sys.argv[:1] + ['test'] + sys.argv[1:]
    execute_from_command_line(argv)
    sys.exit(0)


if __name__ == '__main__':
    runtests()
