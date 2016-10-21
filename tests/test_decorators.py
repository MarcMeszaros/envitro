# -*- coding: utf-8 -*-
# pylint: disable=C0111
import os
import unittest

import envitro


class TestDecorators(unittest.TestCase):

    def test_set_none(self):

        envitro.set('SET', None)
        @envitro.decorators.set('SET', 'myval')
        def myfunc():
            self.assertEqual(os.environ['SET'], 'myval')

        myfunc()
        with self.assertRaises(KeyError):
            os.environ['SET']

    def test_set_string(self):

        os.environ['SET2'] = 'val'
        @envitro.decorators.set('SET2', 'newval')
        def myfunc2():
            self.assertEqual(os.environ['SET2'], 'newval')

        myfunc2()
        self.assertEqual(os.environ['SET2'], 'val')


    def test_isset(self):

        @envitro.decorators.isset('NOT_SET')
        def myfunc():
            return True
        self.assertEqual(myfunc(), None)

        os.environ['SET'] = 'val'
        @envitro.decorators.isset('SET')
        def myfunc2():
            return True
        self.assertTrue(myfunc2())

    def test_bool(self):

        @envitro.decorators.bool('NOT_SET')
        def myfunc():
            return 'returnval'
        self.assertEqual(myfunc(), None)

        os.environ['SET_FALSE'] = 'False'
        @envitro.decorators.bool('SET_FALSE')
        def myfunc2():
            return 'returnval2'
        self.assertEqual(myfunc2(), None)

        os.environ['SET_FALSE_EXEC'] = 'False'
        @envitro.decorators.bool('SET_FALSE_EXEC', execute_bool=False)
        def myfunc3():
            return 'returnval3'
        self.assertEqual(myfunc3(), 'returnval3')

        os.environ['SET_TRUE'] = 'True'
        @envitro.decorators.bool('SET_TRUE')
        def myfunc4():
            return True
        self.assertTrue(myfunc4())

        @envitro.decorators.bool('SET_BOOL_NO_DEFAULT', execute_bool=False)
        def myfunc5():
            return True
        self.assertEqual(myfunc5(), None)

        @envitro.decorators.bool('SET_BOOL_DEFAULT_NO_EXEC', execute_bool=False, default=True)
        def myfunc6():
            return True
        self.assertEqual(myfunc6(), None)

        @envitro.decorators.bool('SET_BOOL_DEFAULT_EXEC', execute_bool=False, default=False)
        def myfunc7():
            return True
        self.assertTrue(myfunc7())
