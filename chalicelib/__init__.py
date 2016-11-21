# coding: utf-8
from __future__ import unicode_literals

import boto3
import os
from chalice import Chalice
from linebot import LineBotApi, WebhookHandler

app = Chalice(app_name='linebot')
app.debug = True

line_bot_api = LineBotApi(os.getenv('LINE_BOT_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_BOT_CHANNEL_ACCESS_SECRET'))

s3_client = boto3.client('s3')
bucket_name = os.getenv('S3_BUCKET_NAME')

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
