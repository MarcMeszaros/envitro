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


def _get_env_value(val, default):
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
    return builtins.str(_get_env_value(val, default))


def bool(val, default=None):
    """
    Gets a string based environment value and returns the Python boolean
    equivalent or default.
    """
    value = _get_env_value(val, default)
    if isinstance(value, builtins.bool):
        return value
    else:
        return builtins.bool(strtobool(builtins.str(value).lower()))


def int(val, default=None):
    """
    Gets a string based environment value and returns the Python integer
    equivalent or default.
    """
    return builtins.int(_get_env_value(val, default))
