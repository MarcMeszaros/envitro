# -*- coding: utf-8 -*-
"""Docker specific environment variable reading.
"""

import re
from os import environ

def _split_docker_link(alias_name):
    """
    Splits a docker link string into a list of 3 items (protocol, host, port).
    - Assumes IPv4 Docker links

    ex: _split_docker_link('DB') -> ['tcp', '172.17.0.82', '8080']
    """
    sanitized_name = alias_name.strip().upper()
    return filter(None, re.split(r':|//', environ.get('{0}_PORT'.format(sanitized_name), '')))


def protocol(alias_name, default='tcp'):
    """
    Get the protocol from the docker link alias or return the default.

    ex: (docker --link postgres:db) -> DB_PORT=tcp://172.17.0.82:5432
    protocol('DB') -> tcp
    """
    try:
        return _split_docker_link(alias_name)[0]
    except Exception as err:
        return default


def host(alias_name, default='127.0.0.1'):
    """
    Get the host from the docker link alias or return the default.

    ex: (docker --link postgres:db) -> DB_PORT=tcp://172.17.0.82:5432
    host('DB') -> 172.17.0.82
    """
    try:
        return _split_docker_link(alias_name)[1]
    except Exception as err:
        return default


def port(alias_name, default=0):
    """
    Get the port from the docker link alias or return the default.

    ex: (docker --link postgres:db) -> DB_PORT=tcp://172.17.0.82:5432
    port('DB') -> 5432
    """
    try:
        return int(_split_docker_link(alias_name)[2])
    except Exception as err:
        return default
