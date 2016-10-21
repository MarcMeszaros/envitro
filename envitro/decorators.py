# -*- coding: utf-8 -*-
# pylint: disable=C0111,W0406,W0622
"""Decorators that modify execution based on environment variables.

A module with decorators that can enable/disable the execution of a function
based on the existance or value of an environment variable. Mostly intended
as a syntactically nice way of enabling/disabling automated tests based on
environment variables.
"""
from __future__ import absolute_import
import functools
import warnings

from . import core


def write(name, value):
    """Temporarily change or set the environment variable during the execution of a function.

    Args:
        name: The name of the environment variable
        value: A value to set for the environment variable

    Returns:
        The function return value.
    """
    def wrapped(func):
        @functools.wraps(func)
        def _decorator(*args, **kwargs):
            existing_env = core.read(name, allow_none=True)
            core.write(name, value)
            func_val = func(*args, **kwargs)
            core.write(name, existing_env)
            return func_val
        return _decorator
    return wrapped


def set(name, value):
    warnings.warn('Will be removed in v1.0', DeprecationWarning, stacklevel=2)
    return write(name, value)


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


def bool(name, execute_bool=True, default=None):
    """Only execute the function if the boolean variable is set.

    Args:
        name: The name of the environment variable
        execute_bool: The boolean value to execute the function on
        default: The default value if the environment variable is not set (respects `execute_bool`)

    Returns:
        The function return value or `None` if the function was skipped.
    """
    def wrapped(func):
        @functools.wraps(func)
        def _decorator(*args, **kwargs):
            if core.isset(name) and core.bool(name) == execute_bool:
                return func(*args, **kwargs)
            elif default is not None and default == execute_bool:
                return func(*args, **kwargs)
        return _decorator
    return wrapped
