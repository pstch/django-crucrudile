#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    :copyright: Copyright 2013 by Hugo Geoffroy
    :contact: hugo@pstch.net
"""


from setuptools import setup


setup(
    name='django-pstch-hlpers',
    version='0.1.0',
    description='Various Django helpers that I use frequently in my projets',
    long_description="views, models, auto URL patterns, ...",
    author='Hugo Geoffroy',
    author_email='hugo@pstch.net',
    packages = ['django_pstch_helpers'],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms=['any'],
)
