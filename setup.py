# -*- coding: utf-8 -*-
# pylint: disable=C0111
from __future__ import absolute_import
import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

from envitro import meta

class ToxTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(args=self.test_args)
        sys.exit(errcode)

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
    tests_require=['tox'],
    cmdclass={
        'test': ToxTest
    },
)
