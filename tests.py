# coding: utf-8
from __future__ import unicode_literals

import app
from unittest import TestCase


class GreetTests(TestCase):
    def test_sleeping_greet(self):
        actual = app._greet('眠たい')
        expected = ['おやすみー', 'おやすみなさい']
        self.assertIn(actual, expected)


class EchoTests(TestCase):
    def test_echo_hello(self):
        actual = app._echo('@bot Hello')
        expected = 'Hello'
        self.assertEqual(actual, expected)


class ChoiceTests(TestCase):
    def test_choice_when_items_separated_by_space(self):
        actual = app._choice('choice a b')
        expected = ['a', 'b']
        self.assertIn(actual, expected)


class ShuffleTests(TestCase):
    def test_shuffle_when_items_separated_by_space(self):
        actual = app._shuffle('shuffle a b')
        expected = ['a\nb', 'b\na']
        self.assertIn(actual, expected)
