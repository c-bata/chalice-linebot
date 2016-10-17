# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

import re
import random

from chalice import Chalice
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Chalice(app_name='linebot')
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_ACCESS_SECRET')


@app.route("/callback", methods=['POST'])
def callback():
    request = app.current_request
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    print('signature: ', signature)

    # get request body as text
    body = request.raw_body.decode('utf-8')
    print('body: ', body)
    handler.handle(body, signature)

    return 'OK'


def _greet(msg):
    greetings = [
        ('眠た?い|ねむた?い|寝る|寝ます', ['おやすみー', 'おやすみなさい']),
        ('いってきま|行ってきま', ['いってらっしゃい', 'いってら']),
        ('こんにち[はわ]', ['こんにちは', 'こんにちは、元気ですかー?']),
        ('おはよう|お早う', ['おはよー', 'おはよう', 'おはようございます！']),
        ('疲れた|つかれた', ['おつかれー', 'おつかれ！', 'お疲れ様！']),
    ]
    for pattern, replies in greetings:
        p = re.compile(pattern)
        if p.match(msg):
            return random.choice(replies)


def _choice(msg):
    prefix = 'choice '
    if msg.startswith(prefix):
        items = msg[len(prefix):].split()
        return random.choice(items)


def _shuffle(msg):
    prefix = 'shuffle '
    if msg.startswith(prefix):
        items = msg[len(prefix):].split()
        random.shuffle(items)
        return '\n'.join(items)


def _echo(msg):
    prefix = '@bot '
    if msg.startswith(prefix):
        return msg[len(prefix):]


plugins = [_greet, _echo, _choice, _shuffle]


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    for plugin in plugins:
        reply = plugin(event.message.text)
        if reply:
            line_bot_api.reply_message(event.reply_token,
                                       messages=TextSendMessage(text=reply))


@app.route('/')
def index():
    return 'pong'
