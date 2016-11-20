# coding: utf-8
from __future__ import unicode_literals

import os
from chalice import Chalice
from linebot import LineBotApi, WebhookHandler

app = Chalice(app_name='linebot')

line_bot_api = LineBotApi(os.environ['LINE_BOT_CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['LINE_BOT_CHANNEL_ACCESS_SECRET'])


HELP_TEXT = """
Commands:
  おはよう, 眠い...
  おみくじ or 今日の運勢
  choice A B
  die
  die カレーメシ
  news
  shuffle A B
  weather
  wiki 単語

Reply:
  @bot ping
  @bot bye
  @bot hey
"""[1:-1]
