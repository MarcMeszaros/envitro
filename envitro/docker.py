# -*- coding: utf-8 -*-
# pylint: disable=W0141,W0406,W0622
"""Docker specific environment variable reading.

A set of functions to read environment variables for docker links.
"""
from __future__ import absolute_import

import re
import warnings

from . import core

def _split_docker_link(alias_name):
    """
    Splits a docker link string into a list of 3 items (protocol, host, port).
    - Assumes IPv4 Docker links

    ex: _split_docker_link('DB') -> ['tcp', '172.17.0.82', '8080']
    """
    sanitized_name = alias_name.strip().upper()
    split_list = re.split(r':|//', core.str('{0}_PORT'.format(sanitized_name)))
    # filter out empty '' vals from the list with filter and
    # cast to list (required for python3)
    return list(filter(None, split_list))

def get(alias_name, allow_none=False):
    """Get the raw docker link value.

    Get the raw environment variable for the docker link

    Args:
        alias_name: The environment variable name
        default: The default value if the link isn't available
        allow_none: If the return value can be `None` (i.e. optional)
    """
    warnings.warn('Will be removed in v1.0', DeprecationWarning, stacklevel=2)
    return core.get('{0}_PORT'.format(alias_name), default=None, allow_none=allow_none)

def isset(alias_name):
    """Return a boolean if the docker link is set or not and is a valid looking docker link value.

    Args:
        alias_name: The link alias name
    """
    warnings.warn('Will be removed in v1.0', DeprecationWarning, stacklevel=2)
    raw_value = get(alias_name, allow_none=True)
    if raw_value:
        if re.compile(r'.+://.+:\d+').match(raw_value):
            return True
        else:
            warnings.warn('"{0}_PORT={1}" does not look like a docker link.'.format(alias_name, raw_value), stacklevel=2)
            return False

    return False

def protocol(alias_name, default=None, allow_none=False):
    """Get the protocol from the docker link alias or return the default.

    Args:
        alias_name: The docker link alias
        default: The default value if the link isn't available
        allow_none: If the return value can be `None` (i.e. optional)

    Examples:
        Assuming a Docker link was created with ``docker --link postgres:db``
        and the resulting environment variable is ``DB_PORT=tcp://172.17.0.82:5432``.

        >>> envitro.docker.protocol('DB')
        tcp
    """
    warnings.warn('Will be removed in v1.0', DeprecationWarning, stacklevel=2)
    try:
        return _split_docker_link(alias_name)[0]
    except KeyError as err:
        if default or allow_none:
            return default
        else:
            raise err


def host(alias_name, default=None, allow_none=False):
    """Get the host from the docker link alias or return the default.

    Args:
        alias_name: The docker link alias
        default: The default value if the link isn't available
        allow_none: If the return value can be `None` (i.e. optional)

    Examples:
        Assuming a Docker link was created with ``docker --link postgres:db``
        and the resulting environment variable is ``DB_PORT=tcp://172.17.0.82:5432``.

        >>> envitro.docker.host('DB')
        172.17.0.82
    """
    warnings.warn('Will be removed in v1.0', DeprecationWarning, stacklevel=2)
    try:
        return _split_docker_link(alias_name)[1]
    except KeyError as err:
        if default or allow_none:
            return default
        else:
            raise err


def port(alias_name, default=None, allow_none=False):
    """Get the port from the docker link alias or return the default.

    Args:
        alias_name: The docker link alias
        default: The default value if the link isn't available
        allow_none: If the return value can be `None` (i.e. optional)

    Examples:
        Assuming a Docker link was created with ``docker --link postgres:db``
        and the resulting environment variable is ``DB_PORT=tcp://172.17.0.82:5432``.

        >>> envitro.docker.port('DB')
        5432
    """
    warnings.warn('Will be removed in v1.0', DeprecationWarning, stacklevel=2)
    try:
        return int(_split_docker_link(alias_name)[2])
    except KeyError as err:
        if default or allow_none:
            return default
        else:
            raise err
