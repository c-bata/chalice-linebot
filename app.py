# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

import re
from random import choice

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


def greet(msg):
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
            return choice(replies)


def _handle_message(message):
    # greeting
    r = greet(message)
    if r:
        return r

    # echo
    prefix = '@bot'
    if message.startswith(prefix):
        return message[len(prefix)+1:]


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply = _handle_message(event.message.text)
    if reply:
        line_bot_api.reply_message(event.reply_token,
                                   messages=TextSendMessage(text=reply))


@app.route('/')
def index():
    return 'Hello'
