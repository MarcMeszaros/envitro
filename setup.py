# -*- coding: utf-8 -*-
# pylint: disable=C0111
from __future__ import absolute_import
import os

from setuptools import setup

from envitro import meta


# Get the long description from the relevant file
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
long_description = None
try:
    with open(os.path.join(BASE_DIR, 'README-pypi.rst')) as f:
        long_description = f.read()
except IOError:
    pass

setup(
    name='envitro',
    version=meta.__version__,
    packages=['envitro'],
    description='A module for reading and writing environment variables.',
    long_description=long_description,
    license='Apache 2',
    author='Marc Meszaros',
    author_email='me@marcmeszaros.com',
    url='https://github.com/MarcMeszaros/envitro',
    keywords=[
        'config', 'environment', '12factor'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'mock'],
    test_suite='tests',
)
