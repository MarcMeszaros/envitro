# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0301,R0904
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

    def test_get_none(self):
        if 'TEST_DEFAULT_GET_NONE' in os.environ:
            del os.environ['TEST_DEFAULT_GET_NONE']
        self.assertEqual(envitro.get('TEST_DEFAULT_GET_NONE', allow_none=True), None)

        if 'TEST_DEFAULT_GET_NONE_DEFAULT' in os.environ:
            del os.environ['TEST_DEFAULT_GET_NONE_DEFAULT']
        self.assertEqual(
            envitro.get('TEST_DEFAULT_GET_NONE_DEFAULT', default='defaultval', allow_none=True), 'defaultval')

    def test_invalid_get(self):
        if 'TEST_INVALID_GET' in os.environ:
            del os.environ['TEST_INVALID_GET']
        self.assertRaises(KeyError, lambda: envitro.get('TEST_INVALID_GET'))

    def test_get(self):
        os.environ['TEST_GET'] = 'getvar'
        self.assertEqual(envitro.get('TEST_GET'), 'getvar')

    def test_invalid(self):
        if 'DOES_NOT_EXIST' in os.environ:
            del os.environ['DOES_NOT_EXIST']
        with self.assertRaises(KeyError):
            envitro.str('DOES_NOT_EXIST')

    def test_nested_default(self):
        self.assertEqual(envitro.int('TEST_NOPE_INT', envitro.str('TEST_NOPE_STR', '123')), 123)
        self.assertEqual(envitro.str('TEST_NOPE_STR', envitro.int('TEST_NOPE_INT', 123)), '123')
        self.assertEqual(envitro.bool('TEST_NOPE_BOOL', envitro.int('TEST_NOPE_INT', 123)), True)
        self.assertEqual(envitro.bool('TEST_NOPE_BOOL', envitro.int('TEST_NOPE_INT', 0)), False)
        self.assertEqual(envitro.bool('TEST_NOPE_BOOL', envitro.int('TEST_NOPE_INT', 123)), True)
        self.assertEqual(envitro.bool('TEST_NOPE_BOOL', envitro.str('TEST_NOPE_STR', 'false')), False)
        self.assertEqual(envitro.bool('TEST_NOPE_BOOL', envitro.str('TEST_NOPE_STR', '')), False)

class TestCoreStr(unittest.TestCase):

    def assert_get_set_str(self, value, expected_value):
        os.environ['TEST_STR'] = value
        self.assertEqual(envitro.str('TEST_STR'), expected_value)

    def test_str(self):
        self.assert_get_set_str('Hello World', 'Hello World')

    def test_str_strip_whitespace(self):
        self.assert_get_set_str('  hello  ', 'hello')


class TestCoreBool(unittest.TestCase):

    def assert_get_set_bool(self, value, expected_value):
        os.environ['TEST_BOOL'] = value
        self.assertEqual(envitro.bool('TEST_BOOL'), expected_value)

    def test_invalid_bool(self):
        envitro.set('INVALID_BOOL', 'nope')
        with self.assertRaises(ValueError):
            envitro.bool('INVALID_BOOL')

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

    def test_default_bool(self):
        if 'DOES_NOT_EXIST' in os.environ:
            del os.environ['DOES_NOT_EXIST']
        self.assertTrue(envitro.bool('DOES_NOT_EXIST', True))
        self.assertFalse(envitro.bool('DOES_NOT_EXIST', False))

    def test_none_bool(self):
        if 'DOES_NOT_EXIST_BOOL' in os.environ:
            del os.environ['DOES_NOT_EXIST_BOOL']
        self.assertEqual(envitro.bool('DOES_NOT_EXIST_BOOL', allow_none=True), None)


class TestCoreInt(unittest.TestCase):

    def assert_get_set_int(self, value, expected_value):
        os.environ['TEST_INT'] = value
        self.assertEqual(envitro.int('TEST_INT'), expected_value)

    def test_int(self):
        self.assert_get_set_int('1234567', 1234567)
        self.assert_get_set_int('  1234567  ', 1234567)


class TestCoreFloat(unittest.TestCase):

    def assert_get_set_float(self, value, expected_value):
        os.environ['TEST_FLOAT'] = value
        self.assertEqual(envitro.float('TEST_FLOAT'), expected_value)

    def test_float(self):
        self.assert_get_set_float('123.45670', 123.4567)
        self.assert_get_set_float('  12345.67  ', 12345.67)
        self.assert_get_set_float('  0012345.67  ', 12345.67)


class TestCoreList(unittest.TestCase):

    def test_list(self):
        os.environ['TEST_LIST'] = 'item1,item2,item3'
        self.assertEqual(envitro.list('TEST_LIST'), ['item1', 'item2', 'item3'])
        os.environ['TEST_LIST'] = 'item1,item2'
        self.assertEqual(envitro.list('TEST_LIST'), ['item1', 'item2'])
        os.environ['TEST_LIST'] = 'item1'
        self.assertEqual(envitro.list('TEST_LIST'), ['item1'])
        os.environ['TEST_LIST'] = 'item1,'
        self.assertEqual(envitro.list('TEST_LIST'), ['item1'])
        os.environ['TEST_LIST'] = ',item1,'
        self.assertEqual(envitro.list('TEST_LIST'), ['item1'])

    def test_list_required(self):
        os.environ['TEST_LIST_REQUIRED'] = ''
        with self.assertRaises(ValueError):
            envitro.list('TEST_LIST_REQUIRED')

    def test_list_spaces(self):
        os.environ['TEST_LIST_SPACES'] = '  item1 , item2 , item3  '
        self.assertEqual(envitro.list('TEST_LIST_SPACES'), ['item1', 'item2', 'item3'])
        os.environ['TEST_LIST_SPACES'] = ' , item1 , item2 , item3 , , ,, '
        self.assertEqual(envitro.list('TEST_LIST_SPACES'), ['item1', 'item2', 'item3'])

    def test_default_list(self):
        if 'DOES_NOT_EXIST' in os.environ:
            del os.environ['DOES_NOT_EXIST']
        self.assertEqual(envitro.list('DOES_NOT_EXIST', ['item1']), ['item1'])
        self.assertEqual(envitro.list('DOES_NOT_EXIST', ['item1', 'item2']), ['item1', 'item2'])
        self.assertEqual(envitro.list('DOES_NOT_EXIST', 'item1,item2'), ['item1', 'item2'])

    def test_list_separator(self):
        os.environ['TEST_LIST_SEPARATOR'] = 'item1;item2;item3'
        self.assertEqual(envitro.list('TEST_LIST_SEPARATOR', separator=';'), ['item1', 'item2', 'item3'])
