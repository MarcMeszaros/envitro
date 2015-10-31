# -*- coding: utf-8 -*-
"""Read environment variables, with casting and optional defaults.

A set of functions to read environment variables and cast them into the correct
python datatypes. Also performs basic error handling.
"""

# Silence "builtin with same name" messages.
# pylint: disable-msg=W0622
try:
    import builtins
except ImportError:
    import __builtin__ as builtins

from os import environ
from .utils import strtobool

def isset(name):
    """
    Return a boolean if the environment variable is set or not.
    """
    return True if environ.get(name) else False

def set(name, value):
    """
    Set the raw env value. A None value clears the environment variable.
    """
    if value is not None:
        environ[name] = value
    elif environ.get(name):
        del environ[name]

def get(val, default=None):
    """
    Get the raw env value, use the default, or throw an exception
    if both the raw value and default are null.
    """
    raw_value = environ.get(val)
    if raw_value or raw_value == '':
        return raw_value
    elif default or (isinstance(default, builtins.int) and default == 0):
        return default
    else:
        raise KeyError('Set the "{0}" environment variable'.format(val))

def str(val, default=None):
    """
    Gets a string based environment value or default.
    """
    return builtins.str(get(val, default).strip())


def bool(val, default=None):
    """
    Gets a string based environment value and returns the Python boolean
    equivalent or default.
    """
    value = get(val, default)
    if isinstance(value, builtins.bool):
        return value
    else:
        return builtins.bool(strtobool(builtins.str(value).lower().strip()))


def int(val, default=None):
    """
    Gets a string based environment value and returns the Python integer
    equivalent or default.
    """
    return builtins.int(get(val, default).strip())
