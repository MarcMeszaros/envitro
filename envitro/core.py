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
        environ[name] = builtins.str(value)
    elif environ.get(name):
        del environ[name]

def get(name, default=None):
    """
    Get the raw env value, use the default, or throw an exception
    if both the raw value and default are null.
    """
    raw_value = environ.get(name)
    if raw_value or raw_value == '':
        return raw_value
    elif default is not None:
        return default
    else:
        raise KeyError('Set the "{0}" environment variable'.format(name))

def str(name, default=None):
    """
    Gets a string based environment value or default.
    """
    return builtins.str(get(name, default)).strip()


def bool(name, default=None):
    """
    Gets a string based environment value and returns the Python boolean
    equivalent or default.
    """
    value = get(name, default)
    if isinstance(value, builtins.bool):
        return value
    elif isinstance(value, builtins.int):
        return True if value > 0 else False
    else:
        value_str = builtins.str(value).lower().strip()
        return strtobool(value_str)


def int(name, default=None):
    """
    Gets a string based environment value and returns the Python integer
    equivalent or default.
    """
    value = get(name, default)
    if isinstance(value, builtins.str):
        value = value.strip()
    return builtins.int(value)
