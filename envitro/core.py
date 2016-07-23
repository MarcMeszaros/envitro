# -*- coding: utf-8 -*-
# pylint: disable=W0141,W0622
"""Read environment variables, with casting and optional defaults.

A set of functions to read environment variables and cast them into the correct
python datatypes. Also performs basic error handling.
"""

try:
    import builtins
except ImportError:
    import __builtin__ as builtins

from os import environ

__all__ = [
    'isset', 'set', 'get', 'int', 'float', 'bool', 'str', 'list'
]

def strtobool(val):
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', '0' and ''.  Raises ValueError if
    'val' is anything else.
    """
    val = val.lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return 1
    elif val in ('n', 'no', 'f', 'false', 'off', '0', ''):
        return 0
    else:
        raise ValueError('Invalid truth value: {0}'.format(val))

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
        allow_none: If the return value can be `None` (i.e. optional)
    """
    raw_value = environ.get(name)
    if raw_value or raw_value == '':
        return raw_value
    elif default is not None or allow_none:
        return default
    else:
        raise KeyError('Set the "{0}" environment variable'.format(name))


def str(name, default=None, allow_none=False):
    """Get a string based environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
        allow_none: If the return value can be `None` (i.e. optional)
    """
    value = get(name, default, allow_none)
    if value is None and allow_none:
        return None
    else:
        return builtins.str(value).strip()


def bool(name, default=None, allow_none=False):
    """Get a boolean based environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
        allow_none: If the return value can be `None` (i.e. optional)
    """
    value = get(name, default, allow_none)
    if isinstance(value, builtins.bool):
        return value
    elif isinstance(value, builtins.int):
        return True if value > 0 else False
    elif value is None and allow_none:
        return None
    else:
        value_str = builtins.str(value).lower().strip()
        return strtobool(value_str)


def int(name, default=None, allow_none=False):
    """Get a string environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
        allow_none: If the return value can be `None` (i.e. optional)
    """
    value = get(name, default, allow_none)
    if isinstance(value, builtins.str):
        value = value.strip()

    if value is None and allow_none:
        return None
    else:
        return builtins.int(value)


def float(name, default=None, allow_none=False):
    """Get a string environment value or the default.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
        allow_none: If the return value can be `None` (i.e. optional)
    """
    value = get(name, default, allow_none)
    if isinstance(value, builtins.str):
        value = value.strip()

    if value is None and allow_none:
        return None
    else:
        return builtins.float(value)


def list(name, default=None, allow_none=False, separator=','):
    """Get a list of strings or the default.

    The individual list elements are whitespace-stripped.

    Args:
        name: The environment variable name
        default: The default value to use if no environment variable is found
        allow_none: If the return value can be `None` (i.e. optional)
        separator: The list item separator character or pattern
    """
    value = get(name, default, allow_none)
    if isinstance(value, builtins.list):
        return value
    elif isinstance(value, builtins.str):
        value_list = [item.strip() for item in value.split(separator)]
        value_list_sanitized = builtins.list(filter(None, value_list))
        if len(value_list_sanitized) > 0:
            return value_list_sanitized
        else:
            raise ValueError('Invalid list variable.')
    elif value is None and allow_none:
        return None
    else:
        return [builtins.str(value)]
