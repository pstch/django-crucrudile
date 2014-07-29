#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Hugo Geoffroy
    :contact: hugo@pstch.net
"""

from setuptools import setup, find_packages
import os

import django_crucrudile

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]

setup(
    name=django_crucrudile.__title__,
    version=django_crucrudile.__version__,
    description='Define URL patterns in DJango models',

    url=django_crucrudile.__url__,

    author=django_crucrudile.__author__,
    author_email=django_crucrudile.__author_email__,

    license=django_crucrudile.__license__,

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'django == 1.6'
    ],
    tests_require=[
        'mock',
        'nose',
        'coverage',
    ],
    classifiers=CLASSIFIERS,
    download_url=('https://github.com/pstch/django-crucrudile/tarball/v' +
                  django_crucrudile.__version__),
    test_suite='nose.collector',
)
