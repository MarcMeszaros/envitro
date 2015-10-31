# -*- coding: utf-8 -*-
"""Unit tests for the envitro module."""

import unittest
import os
import envitro
import envitro.docker

class TestDocker(unittest.TestCase):

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

    def test_port(self):
        envitro.set('DB_PORT', 'tcp://172.17.0.82:5432')
        self.assertEqual(envitro.docker.port('DB'), 5432)

    def test_protocol_required(self):
        if envitro.isset('DB_REQUIRED_PORT'):
            del os.environ['DB_REQUIRED_PORT']
        with self.assertRaises(KeyError):
            envitro.docker.port('DB_REQUIRED_PORT')

    def test_port_default(self):
        if envitro.isset('DB_DEFAULT_PORT'):
            del os.environ['DB_DEFAULT_PORT']
        self.assertEqual(envitro.docker.port('DB_DEFAULT', 1234), 1234)
