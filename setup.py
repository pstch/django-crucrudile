#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Hugo Geoffroy
    :contact: hugo@pstch.net
"""

from setuptools import setup, find_packages

import django_crucrudile

CLASSIFIERS = [
    'Framework :: Django',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Topic :: Software Development',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
]

setup(
    name=django_crucrudile.__title__,
    version=django_crucrudile.__version__,


    url=django_crucrudile.__url__,

    author=django_crucrudile.__author__,
    author_email=django_crucrudile.__author_email__,

    license=django_crucrudile.__license__,

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'Django == 1.6'
    ],

    classifiers=CLASSIFIERS,

    test_suite='runtests.runtests',
)
