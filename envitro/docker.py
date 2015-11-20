# -*- coding: utf-8 -*-
"""Docker specific environment variable reading.

A set of functions to read environment variables for docker links.
"""
from __future__ import absolute_import

# Silence "builtin with same name" messages.
# pylint: disable-msg=W0622
import re
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

def isset(alias_name):
    """Return a boolean if the docker link is set or not.

    Args:
        name: The link alias name
    """
    return core.isset('{0}_PORT'.format(alias_name))

def get(alias_name):
    """Get the raw docker link value.

    Get the raw environment variable for the docker link

    Args:
        alias_name: The environment variable name
    """
    return core.get('{0}_PORT'.format(alias_name), default=None, allow_none=True)

def protocol(alias_name, default=None):
    """Get the protocol from the docker link alias or return the default.

    Args:
        alias_name: The docker link alias

    Examples:
        Assuming a Docker link was created with ``docker --link postgres:db``
        and the resulting environment variable is ``DB_PORT=tcp://172.17.0.82:5432``.

        >>> envitro.docker.protocol('DB')
        tcp
    """
    try:
        return _split_docker_link(alias_name)[0]
    except KeyError as err:
        if default:
            return default
        else:
            raise err


def host(alias_name, default=None):
    """Get the host from the docker link alias or return the default.

    Args:
        alias_name: The docker link alias

    Examples:
        Assuming a Docker link was created with ``docker --link postgres:db``
        and the resulting environment variable is ``DB_PORT=tcp://172.17.0.82:5432``.

        >>> envitro.docker.host('DB')
        172.17.0.82
    """
    try:
        return _split_docker_link(alias_name)[1]
    except KeyError as err:
        if default:
            return default
        else:
            raise err


def port(alias_name, default=None):
    """Get the port from the docker link alias or return the default.

    Args:
        alias_name: The docker link alias

    Examples:
        Assuming a Docker link was created with ``docker --link postgres:db``
        and the resulting environment variable is ``DB_PORT=tcp://172.17.0.82:5432``.

        >>> envitro.docker.port('DB')
        5432
    """
    try:
        return int(_split_docker_link(alias_name)[2])
    except KeyError as err:
        if default:
            return default
        else:
            raise err
