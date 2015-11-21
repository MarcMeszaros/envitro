# -*- coding: utf-8 -*-
"""Unit tests for the envitro module."""

# Silence some pylint messages.
# pylint: disable=C0111

import os
import unittest

import envitro
import envitro.docker

class TestDocker(unittest.TestCase):

    def test_isset(self):
        envitro.set('DB_PORT', 'tcp://172.17.0.82:5432')
        self.assertTrue(envitro.docker.isset('DB'))
        envitro.set('NODB_PORT', None)
        self.assertFalse(envitro.docker.isset('NODB'))

    def test_get(self):
        envitro.set('DB_PORT', 'tcp://172.17.0.82:5432')
        self.assertEqual(envitro.docker.get('DB'), 'tcp://172.17.0.82:5432')
        envitro.set('NODB_PORT', None)
        self.assertEqual(envitro.docker.get('NODB', allow_none=True), None)

    def test_protocol(self):
        envitro.set('DB_PORT', 'tcp://172.17.0.82:5432')
        self.assertEqual(envitro.docker.protocol('DB'), 'tcp')

    def test_protocol_required(self):
        if envitro.isset('DB_REQUIRED_PORT'):
            del os.environ['DB_REQUIRED_PORT']
        with self.assertRaises(KeyError):
            envitro.docker.protocol('DB_REQUIRED_PORT')

    def test_protocol_default(self):
        if envitro.isset('DB_DEFAULT_PORT'):
            del os.environ['DB_DEFAULT_PORT']
        self.assertEqual(envitro.docker.protocol('DB_DEFAULT', 'udp'), 'udp')

    def test_protocol_none(self):
        if envitro.isset('DB_DEFAULT_NONE_PORT'):
            del os.environ['DB_DEFAULT_NONE_PORT']
        self.assertEqual(envitro.docker.protocol('DB_DEFAULT_NONE', allow_none=True), None)

    def test_host(self):
        envitro.set('DB_PORT', 'tcp://172.17.0.82:5432')
        self.assertEqual(envitro.docker.host('DB'), '172.17.0.82')

    def test_host_required(self):
        if envitro.isset('DB_REQUIRED_PORT'):
            del os.environ['DB_REQUIRED_PORT']
        with self.assertRaises(KeyError):
            envitro.docker.host('DB_REQUIRED_PORT')

    def test_host_default(self):
        if envitro.isset('DB_DEFAULT_PORT'):
            del os.environ['DB_DEFAULT_PORT']
        self.assertEqual(envitro.docker.host('DB_DEFAULT', 'localhost'), 'localhost')

    def test_host_none(self):
        if envitro.isset('DB_DEFAULT_NONE_PORT'):
            del os.environ['DB_DEFAULT_NONE_PORT']
        self.assertEqual(envitro.docker.host('DB_DEFAULT_NONE', allow_none=True), None)

    def test_port(self):
        envitro.set('DB_PORT', 'tcp://172.17.0.82:5432')
        self.assertEqual(envitro.docker.port('DB'), 5432)

    def test_port_required(self):
        if envitro.isset('DB_REQUIRED_PORT'):
            del os.environ['DB_REQUIRED_PORT']
        with self.assertRaises(KeyError):
            envitro.docker.port('DB_REQUIRED_PORT')

    def test_port_default(self):
        if envitro.isset('DB_DEFAULT_PORT'):
            del os.environ['DB_DEFAULT_PORT']
        self.assertEqual(envitro.docker.port('DB_DEFAULT', 1234), 1234)

    def test_port_none(self):
        if envitro.isset('DB_DEFAULT_NONE_PORT'):
            del os.environ['DB_DEFAULT_NONE_PORT']
        self.assertEqual(envitro.docker.port('DB_DEFAULT_NONE', allow_none=True), None)
