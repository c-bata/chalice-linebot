# coding: utf-8
from __future__ import unicode_literals

from app import greet, _handle_message
from unittest import TestCase


class GreetingTests(TestCase):
    def test_sleeping_greet(self):
        actual = greet('眠たい')
        expected = ['おやすみー', 'おやすみなさい']
        self.assertIn(actual, expected)


class HandleMessageTests(TestCase):
    def test_sleeping_greet(self):
        actual = _handle_message('眠たい')
        expected = ['おやすみー', 'おやすみなさい']
        self.assertIn(actual, expected)

    def test_echo(self):
        actual = _handle_message('@bot Hello')
        expected = 'Hello'
        self.assertEqual(actual, expected)
