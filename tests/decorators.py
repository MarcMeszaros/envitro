# -*- coding: utf-8 -*-

# Silence some pylint messages.
# pylint: disable=C0111

import os
import unittest

from envitro import decorators


class TestDecorators(unittest.TestCase):

    def test_isset(self):

        @decorators.isset('NOT_SET')
        def myfunc():
            return True
        self.assertEqual(myfunc(), None)

        os.environ['SET'] = 'val'
        @decorators.isset('SET')
        def myfunc2():
            return True
        self.assertTrue(myfunc2())

    def test_bool(self):

        @decorators.bool('NOT_SET')
        def myfunc():
            return 'returnval'
        self.assertEqual(myfunc(), None)

        os.environ['SET_FALSE'] = 'False'
        @decorators.bool('SET_FALSE')
        def myfunc2():
            return 'returnval2'
        self.assertEqual(myfunc2(), None)

        os.environ['SET_FALSE_EXEC'] = 'False'
        @decorators.bool('SET_FALSE_EXEC', execute_bool=False)
        def myfunc3():
            return 'returnval3'
        self.assertEqual(myfunc3(), 'returnval3')

        os.environ['SET_TRUE'] = 'True'
        @decorators.bool('SET_TRUE')
        def myfunc4():
            return True
        self.assertTrue(myfunc4())
