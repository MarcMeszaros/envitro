# -*- coding: utf-8 -*-
"""Unit tests for the envitro module."""

import unittest
import os
import envitro


class TestCore(unittest.TestCase):

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
        self.assertRaises(KeyError, lambda: envitro.str('DOES_NOT_EXIST'))

    def test_invalid_bool(self):
        os.environ['INVALID_BOOL'] = 'nope'
        self.assertRaises(ValueError, lambda: envitro.bool('INVALID_BOOL'))
