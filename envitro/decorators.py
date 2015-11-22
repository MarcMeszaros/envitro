# -*- coding: utf-8 -*-
"""Decorators that modify execution based on environment variables.

A module with decorators that can enable/disable the execution of a function
based on the existance or value of an environment variable. Mostly intended
as a syntactically nice way of enabling/disabling automated tests based on
environment variables.
"""

# Silence some pylint messages.
# pylint: disable=W0622,W0406,C0111

import functools

from . import core

def isset(name):
    """Only execute the function if the variable is set.

    Args:
        name: The name of the environment variable

    Returns:
        The function return value or `None` if the function was skipped.
    """
    def wrapped(func):
        @functools.wraps(func)
        def _decorator(*args, **kwargs):
            if core.isset(name):
                return func(*args, **kwargs)
        return _decorator
    return wrapped

def bool(name, execute_bool=True):
    """Only execute the function if the boolean variable is set.

    Args:
        name: The name of the environment variable
        execute_bool: The boolean value to execute the function on

    Returns:
        The function return value or `None` if the function was skipped.
    """
    def wrapped(func):
        @functools.wraps(func)
        def _decorator(*args, **kwargs):
            if core.isset(name) and core.bool(name) == execute_bool:
                return func(*args, **kwargs)
        return _decorator
    return wrapped
