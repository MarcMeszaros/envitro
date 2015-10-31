# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = 'envitro',
    version = '0.1.0',
    packages = find_packages(exclude=['tests']),
    description = 'A module to read environment variables.',
    license = 'Apache 2',
    author = 'Marc Meszaros',
    author_email = 'me@marcmeszaros.com',
    url = 'https://github.com/MarcMeszaros/envitro',
    keywords = [
        'config', 'environment', '12factor'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite = 'envitro.tests',
)
