# -*- coding: utf-8 -*-
# pylint: disable=C0111
import os
import unittest

import envitro


class TestSetDecorator(unittest.TestCase):

    def tearDown(self):
        if 'ENV_VAL' in os.environ:
            del os.environ['ENV_VAL']

    def test_set_none(self):

        envitro.set('ENV_VAL', None)
        @envitro.decorators.set('ENV_VAL', 'myval')
        def myfunc():
            self.assertEqual(os.environ['ENV_VAL'], 'myval')

        myfunc()
        with self.assertRaises(KeyError):
            os.environ['ENV_VAL']

    def test_set_string(self):

        os.environ['ENV_VAL'] = 'val'
        @envitro.decorators.set('ENV_VAL', 'newval')
        def myfunc():
            self.assertEqual(os.environ['ENV_VAL'], 'newval')

        myfunc()
        self.assertEqual(os.environ['ENV_VAL'], 'val')


class TestIsSetDecorator(unittest.TestCase):

    def tearDown(self):
        if 'ENV_VAL' in os.environ:
            del os.environ['ENV_VAL']

    def test_isset(self):
        os.environ['ENV_VAL'] = 'val'
        @envitro.decorators.isset('ENV_VAL')
        def myfunc():
            return True
        self.assertTrue(myfunc())

    def test_isset_false(self):
        @envitro.decorators.isset('ENV_VAL')
        def myfunc():
            return True
        self.assertEqual(myfunc(), None)


class TestBoolDecorator(unittest.TestCase):

    def tearDown(self):
        if 'ENV_VAL' in os.environ:
            del os.environ['ENV_VAL']

    def test_bool_execute(self):

        @envitro.decorators.bool('ENV_VAL')
        def myfunc():
            return 'returnval'
        self.assertEqual(myfunc(), None)

    def test_bool_no_execute(self):
        os.environ['ENV_VAL'] = 'False'
        @envitro.decorators.bool('ENV_VAL')
        def myfunc():
            return 'returnval'
        self.assertEqual(myfunc(), None)

    def test_bool_execute_value(self):
        os.environ['ENV_VAL'] = 'False'
        @envitro.decorators.bool('ENV_VAL', execute_bool=False)
        def myfunc():
            return 'returnval'
        self.assertEqual(myfunc(), 'returnval')

    def test_bool_execute_value_no_execute(self):
        @envitro.decorators.bool('ENV_VAL', execute_bool=False)
        def myfunc():
            return True
        self.assertEqual(myfunc(), None)

    def test_bool_execute_value_default_execute(self):
        @envitro.decorators.bool('ENV_VAL_DEFAULT_NO_EXEC', execute_bool=False, default=False)
        def myfunc():
            return True
        self.assertTrue(myfunc())

    def test_bool_execute_value_default_no_execute(self):
        @envitro.decorators.bool('ENV_VAL_DEFAULT_NO_EXEC', execute_bool=False, default=True)
        def myfunc():
            return True
        self.assertEqual(myfunc(), None)
