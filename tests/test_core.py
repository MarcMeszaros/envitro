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

    def test_write(self):
        envitro.write('TEST_SET', 'setvar')
        self.assertEqual(os.environ['TEST_SET'], 'setvar')
        envitro.write('TEST_SET_SPACES', '  spacesvar  ')
        self.assertEqual(os.environ['TEST_SET_SPACES'], '  spacesvar  ')
        envitro.write('TEST_SET_INT', 123)
        self.assertEqual(os.environ['TEST_SET_INT'], '123')
        envitro.write('TEST_SET_BOOL', True)
        self.assertEqual(os.environ['TEST_SET_BOOL'], 'True')

    def test_write_clear(self):
        os.environ['TEST_ALREADY_SET'] = 'myvar'
        envitro.write('TEST_ALREADY_SET', None)
        self.assertEqual(os.environ.get('TEST_ALREADY_SET'), None)

        if 'TEST_ALREADY_SET_MISSING' in os.environ:
            del os.environ['TEST_ALREADY_SET_MISSING']
        envitro.write('TEST_ALREADY_SET_MISSING', None)
        self.assertEqual(os.environ.get('TEST_ALREADY_SET_MISSING'), None)

    def test_read_default(self):
        if 'TEST_DEFAULT_GET' in os.environ:
            del os.environ['TEST_DEFAULT_GET']
        self.assertEqual(envitro.read('TEST_DEFAULT_GET', 'defaultval'), 'defaultval')

    def test_read_none(self):
        if 'TEST_DEFAULT_GET_NONE' in os.environ:
            del os.environ['TEST_DEFAULT_GET_NONE']
        self.assertEqual(envitro.read('TEST_DEFAULT_GET_NONE', allow_none=True), None)

        if 'TEST_DEFAULT_GET_NONE_DEFAULT' in os.environ:
            del os.environ['TEST_DEFAULT_GET_NONE_DEFAULT']
        self.assertEqual(
            envitro.read('TEST_DEFAULT_GET_NONE_DEFAULT', default='defaultval', allow_none=True), 'defaultval')

    def test_read_fallback(self):
        if 'TEST_PRIMARY' in os.environ:
            del os.environ['TEST_PRIMARY']
        self.assertEqual(envitro.read('TEST_PRIMARY', allow_none=True), None)

        os.environ['TEST_FALLBACK'] = 'fallback'
        self.assertEqual(envitro.read('TEST_PRIMARY', fallback='TEST_FALLBACK'), 'fallback')

    def test_read_fallback_list(self):
        if 'TEST_PRIMARY' in os.environ:
            del os.environ['TEST_PRIMARY']
        if 'TEST_FALLBACK_1' in os.environ:
            del os.environ['TEST_FALLBACK_1']

        os.environ['TEST_FALLBACK_2'] = 'fallback2'
        self.assertEqual(envitro.read('TEST_PRIMARY', fallback=['TEST_FALLBACK_1', 'TEST_FALLBACK_2']), 'fallback2')

    def test_read_fallback_list_default(self):
        if 'TEST_PRIMARY' in os.environ:
            del os.environ['TEST_PRIMARY']
        if 'TEST_FALLBACK_1' in os.environ:
            del os.environ['TEST_FALLBACK_1']
        if 'TEST_FALLBACK_2' in os.environ:
            del os.environ['TEST_FALLBACK_2']

        self.assertEqual(envitro.read('TEST_PRIMARY', default='def', fallback=['TEST_FALLBACK_1', 'TEST_FALLBACK_2']), 'def')

    def test_invalid_read(self):
        if 'TEST_INVALID_GET' in os.environ:
            del os.environ['TEST_INVALID_GET']
        self.assertRaises(KeyError, lambda: envitro.read('TEST_INVALID_GET'))

    def test_read(self):
        os.environ['TEST_GET'] = 'getvar'
        self.assertEqual(envitro.read('TEST_GET'), 'getvar')

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

    def test_none_str(self):
        if 'DOES_NOT_EXIST_STR' in os.environ:
            del os.environ['DOES_NOT_EXIST_STR']
        self.assertEqual(envitro.str('DOES_NOT_EXIST_STR', allow_none=True), None)

    def test_fallback(self):
        if 'PRIMARY' in os.environ:
            del os.environ['PRIMARY']

        os.environ['FALLBACK'] = ' fallback'
        self.assertEqual(envitro.str('PRIMARY', fallback='FALLBACK'), 'fallback')


class TestCoreBool(unittest.TestCase):

    def assert_get_set_bool(self, value, expected_value):
        os.environ['TEST_BOOL'] = value
        self.assertEqual(envitro.bool('TEST_BOOL'), expected_value)

    def test_invalid_bool(self):
        envitro.write('INVALID_BOOL', 'nope')
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

    def test_fallback(self):
        if 'PRIMARY' in os.environ:
            del os.environ['PRIMARY']

        os.environ['FALLBACK'] = ' true'
        self.assertEqual(envitro.bool('PRIMARY', fallback='FALLBACK'), True)



class TestCoreInt(unittest.TestCase):

    def assert_get_set_int(self, value, expected_value):
        os.environ['TEST_INT'] = value
        self.assertEqual(envitro.int('TEST_INT'), expected_value)

    def test_int(self):
        self.assert_get_set_int('1234567', 1234567)
        self.assert_get_set_int('  1234567  ', 1234567)

    def test_none_int(self):
        if 'DOES_NOT_EXIST_INT' in os.environ:
            del os.environ['DOES_NOT_EXIST_INT']
        self.assertEqual(envitro.int('DOES_NOT_EXIST_INT', allow_none=True), None)

    def test_fallback(self):
        if 'PRIMARY' in os.environ:
            del os.environ['PRIMARY']

        os.environ['FALLBACK'] = ' 5'
        self.assertEqual(envitro.int('PRIMARY', fallback='FALLBACK'), 5)


class TestCoreFloat(unittest.TestCase):

    def assert_get_set_float(self, value, expected_value):
        os.environ['TEST_FLOAT'] = value
        self.assertEqual(envitro.float('TEST_FLOAT'), expected_value)

    def test_float(self):
        self.assert_get_set_float('123.45670', 123.4567)
        self.assert_get_set_float('  12345.67  ', 12345.67)
        self.assert_get_set_float('  0012345.67  ', 12345.67)

    def test_none_float(self):
        if 'DOES_NOT_EXIST_FLOAT' in os.environ:
            del os.environ['DOES_NOT_EXIST_FLOAT']
        self.assertEqual(envitro.float('DOES_NOT_EXIST_FLOAT', allow_none=True), None)

    def test_fallback(self):
        if 'PRIMARY' in os.environ:
            del os.environ['PRIMARY']

        os.environ['FALLBACK'] = ' 3.14'
        self.assertEqual(envitro.float('PRIMARY', fallback='FALLBACK'), 3.14)


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

    def test_none_list(self):
        if 'DOES_NOT_EXIST_LIST' in os.environ:
            del os.environ['DOES_NOT_EXIST_LIST']
        self.assertEqual(envitro.list('DOES_NOT_EXIST_LIST', allow_none=True), None)

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

    def test_fallback(self):
        if 'PRIMARY' in os.environ:
            del os.environ['PRIMARY']

        os.environ['FALLBACK'] = ' a,b,c'
        self.assertEqual(envitro.list('PRIMARY', fallback='FALLBACK'), ['a', 'b', 'c'])


class TestCoreTuple(unittest.TestCase):

    def test_tuple(self):
        os.environ['TEST_TUPLE'] = 'item1,item2,item3'
        self.assertEqual(envitro.tuple('TEST_TUPLE'), ('item1', 'item2', 'item3'))
        os.environ['TEST_TUPLE'] = 'item1,item2'
        self.assertEqual(envitro.tuple('TEST_TUPLE'), ('item1', 'item2'))
        os.environ['TEST_TUPLE'] = 'item1'
        self.assertEqual(envitro.tuple('TEST_TUPLE'), ('item1', ))
        os.environ['TEST_TUPLE'] = 'item1,'
        self.assertEqual(envitro.tuple('TEST_TUPLE'), ('item1', ))
        os.environ['TEST_TUPLE'] = ',item1,'
        self.assertEqual(envitro.tuple('TEST_TUPLE'), ('item1', ))

    def test_tuple_required(self):
        os.environ['TEST_TUPLE_REQUIRED'] = ''
        with self.assertRaises(ValueError):
            envitro.tuple('TEST_TUPLE_REQUIRED')

    def test_none_tuple(self):
        if 'DOES_NOT_EXIST_TUPLE' in os.environ:
            del os.environ['DOES_NOT_EXIST_TUPLE']
        self.assertEqual(envitro.tuple('DOES_NOT_EXIST_TUPLE', allow_none=True), None)

    def test_tuple_spaces(self):
        os.environ['TEST_TUPLE_SPACES'] = '  item1 , item2 , item3  '
        self.assertEqual(envitro.tuple('TEST_LIST_SPACES'), ('item1', 'item2', 'item3'))
        os.environ['TEST_TUPLE_SPACES'] = ' , item1 , item2 , item3 , , ,, '
        self.assertEqual(envitro.tuple('TEST_TUPLE_SPACES'), ('item1', 'item2', 'item3'))

    def test_default_tuple(self):
        if 'DOES_NOT_EXIST' in os.environ:
            del os.environ['DOES_NOT_EXIST']
        self.assertEqual(envitro.tuple('DOES_NOT_EXIST', ('item1', )), ('item1', ))
        self.assertEqual(envitro.tuple('DOES_NOT_EXIST', ('item1', 'item2')), ('item1', 'item2'))
        self.assertEqual(envitro.tuple('DOES_NOT_EXIST', 'item1,item2'), ('item1', 'item2'))

    def test_tuple_separator(self):
        os.environ['TEST_TUPLE_SEPARATOR'] = 'item1;item2;item3'
        self.assertEqual(envitro.tuple('TEST_TUPLE_SEPARATOR', separator=';'), ('item1', 'item2', 'item3'))

    def test_fallback(self):
        if 'PRIMARY' in os.environ:
            del os.environ['PRIMARY']

        os.environ['FALLBACK'] = ' a,b,c'
        self.assertEqual(envitro.tuple('PRIMARY', fallback='FALLBACK'), ('a', 'b', 'c'))
