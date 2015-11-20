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
    """Return a boolean if the environment variable is set or not.

    Args:
        name: The environment variable name
    """
    return True if environ.get(name) else False

def set(name, value):
    """Set a raw env value.

    A ``None`` value clears the environment variable.

    Args:
        name: The environment variable name
        value: The value to set
    """
    if value is not None:
        environ[name] = builtins.str(value)
    elif environ.get(name):
        del environ[name]

def get(name, default=None, allow_none=False):
    """Get the raw env value.

    Get the raw environment variable or use the default. If the value is not
    found and no default is set throw an exception.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
    """
    raw_value = environ.get(name)
    if raw_value or raw_value == '':
        return raw_value
    elif default is not None or allow_none:
        return default
    else:
        raise KeyError('Set the "{0}" environment variable'.format(name))


def str(name, default=None):
    """Get a string based environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
    """
    return builtins.str(get(name, default)).strip()


def bool(name, default=None):
    """Get a boolean based environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
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
    """Get a string environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
    """
    value = get(name, default)
    if isinstance(value, builtins.str):
        value = value.strip()
    return builtins.int(value)


def float(name, default=None):
    """Get a string environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
    """
    value = get(name, default)
    if isinstance(value, builtins.str):
        value = value.strip()
    return builtins.float(value)


def list(name, default=None, separator=','):
    """Get a list of strings or the default.

    The individual list elements are whitespace-stripped.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
        separator: The list item separator character or pattern
    """
    value = get(name, default)
    if isinstance(value, builtins.list):
        return value
    elif isinstance(value, builtins.str):
        value_list = [item.strip() for item in value.split(separator)]
        value_list_sanitized = builtins.list(filter(None, value_list))
        if len(value_list_sanitized) > 0:
            return value_list_sanitized
        else:
            raise ValueError('Invalid list variable.')
    else:
        return [builtins.str(value)]
