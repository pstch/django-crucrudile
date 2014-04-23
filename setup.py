#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Hugo Geoffroy
    :contact: hugo@pstch.net
"""

from setuptools import setup, find_packages

import django_crucrudile

setup(
    name='django-crucrudile',
    version=django_crucrudile.__version__,

    description='Model-defined CRUD views & patterns for Django',
    long_description="views, models, auto URL patterns, ...",

    url='https://github.com/pstch/django-crucrudile',

    author='Hugo Geoffroy',
    author_email='hugo@pstch.net',

    packages=find_packages(exclude=['tests']),
    install_requires=[
        'Django == 1.6'
    ],

    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
    ],
    platforms=['any'],

    test_suite='runtests.runtests',
)
