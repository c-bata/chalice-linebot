# coding: utf-8
from __future__ import unicode_literals

from chalicelib import bot_utils
from unittest import TestCase


class SuddenDeathTests(TestCase):
    def test_sudden_death(self):
        actual = bot_utils.sudden_death('突然の死')
        expected = """
＿人人人人人人＿
＞  突然の死  ＜
￣Y^Y^Y^Y^Y￣
"""[1:-1]
        self.assertIn(actual, expected)
