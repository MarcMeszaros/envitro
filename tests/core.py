# -*- coding: utf-8 -*-
"""Unit tests for the envitro module."""

import unittest
import os
import envitro


class TestCore(unittest.TestCase):

    # test setter/getter
    def test_isset(self):
        os.environ['TEST_ISSET_TRUE'] = 'setvar'
        self.assertTrue(envitro.isset('TEST_ISSET_TRUE'))

        if 'TEST_ISSET_FALSE' in os.environ:
            del os.environ['TEST_ISSET_FALSE']
        self.assertFalse(envitro.isset('TEST_ISSET_FALSE'))

    def test_set(self):
        envitro.set('TEST_SET', 'setvar')
        self.assertEqual(os.environ['TEST_SET'], 'setvar')
        envitro.set('TEST_SET_SPACES', '  spacesvar  ')
        self.assertEqual(os.environ['TEST_SET_SPACES'], '  spacesvar  ')
        envitro.set('TEST_SET_INT', 123)
        self.assertEqual(os.environ['TEST_SET_INT'], '123')
        envitro.set('TEST_SET_BOOL', True)
        self.assertEqual(os.environ['TEST_SET_BOOL'], 'True')

    def test_set_clear(self):
        os.environ['TEST_ALREADY_SET'] = 'myvar'
        envitro.set('TEST_ALREADY_SET', None)
        self.assertEqual(os.environ.get('TEST_ALREADY_SET'), None)

        if 'TEST_ALREADY_SET_MISSING' in os.environ:
            del os.environ['TEST_ALREADY_SET_MISSING']
        envitro.set('TEST_ALREADY_SET_MISSING', None)
        self.assertEqual(os.environ.get('TEST_ALREADY_SET_MISSING'), None)

    def test_get_default(self):
        if 'TEST_DEFAULT_GET' in os.environ:
            del os.environ['TEST_DEFAULT_GET']
        self.assertEqual(envitro.get('TEST_DEFAULT_GET', 'defaultval'), 'defaultval')

    def test_invalid_get(self):
        if 'TEST_INVALID_GET' in os.environ:
            del os.environ['TEST_INVALID_GET']
        self.assertRaises(KeyError, lambda: envitro.get('TEST_INVALID_GET'))

    def test_get(self):
        os.environ['TEST_GET'] = 'getvar'
        self.assertEqual(envitro.get('TEST_GET'), 'getvar')

    # helper testing functions
    def assert_get_set_bool(self, value, expected_value):
        os.environ['TEST_BOOL'] = value
        self.assertEqual(envitro.bool('TEST_BOOL'), expected_value)

    def assert_get_set_str(self, value, expected_value):
        os.environ['TEST_STR'] = value
        self.assertEqual(envitro.str('TEST_STR'), expected_value)

    def assert_get_set_int(self, value, expected_value):
        os.environ['TEST_INT'] = value
        self.assertEqual(envitro.int('TEST_INT'), expected_value)

    # actual tests
    def test_str(self):
        self.assert_get_set_str('Hello World', 'Hello World')

    def test_str_strip_whitespace(self):
        self.assert_get_set_str('  hello  ', 'hello')

    def test_int(self):
        self.assert_get_set_int('1234567', 1234567)
        self.assert_get_set_int('  1234567  ', 1234567)

    def test_bool(self):
        self.assert_get_set_bool('yes', True)
        self.assert_get_set_bool('1', True)
        self.assert_get_set_bool('YeS', True)
        self.assert_get_set_bool('True', True)
        self.assert_get_set_bool('true', True)
        self.assert_get_set_bool(' 1 ', True)
        self.assert_get_set_bool('YES\t', True)
        self.assert_get_set_bool('\tYES\t', True)
        self.assert_get_set_bool('false', False)
        self.assert_get_set_bool('no', False)
        self.assert_get_set_bool('0', False)
        self.assert_get_set_bool('  NO  ', False)
        self.assert_get_set_bool('', False)
        self.assert_get_set_bool(' ', False)

    def test_invalid(self):
        if 'DOES_NOT_EXIST' in os.environ:
            del os.environ['DOES_NOT_EXIST']
        with self.assertRaises(KeyError):
            envitro.str('DOES_NOT_EXIST')

    def test_invalid_bool(self):
        envitro.set('INVALID_BOOL', 'nope')
        with self.assertRaises(ValueError):
            envitro.bool('INVALID_BOOL')
