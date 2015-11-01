# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from envitro import __VERSION__

class ToxTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errcode = tox.cmdline(args=self.test_args)
        sys.exit(errcode)

setup(
    name = 'envitro',
    version = __VERSION__,
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
    tests_require = ['tox'],
    cmdclass={'test': ToxTest},
)
