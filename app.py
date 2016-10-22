# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

import re
import random

from chalice import Chalice
import feedparser
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, URITemplateAction,
)
import requests

app = Chalice(app_name='linebot')
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_ACCESS_SECRET')


@app.route('/')
def index():
    return 'pong'


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
        ('ぽやしみ|おやすみ|眠た?い|ねむた?い|寝る|寝ます', ['おやすみー', 'おやすみなさい']),
        ('いってきま|行ってきま', ['いってらっしゃい', 'いってら']),
        ('こんにち[はわ]', ['こんにちは', 'こんにちは、元気ですかー?']),
        ('おはよう|お早う', ['おはよー', 'おはよう', 'おはようございます！']),
        ('疲れた|つかれた', ['おつかれー', 'おつかれ！', 'お疲れ様！']),
    ]
    for pattern, replies in greetings:
        if re.match(pattern, msg):
            return TextSendMessage(text=random.choice(replies))


def _choice(msg):
    if re.match('^[cC]hoice.*', msg):
        items = msg[len('choice '):].split()
        return TextSendMessage(random.choice(items))


def _shuffle(msg):
    if re.match('^[sS]huffle.*', msg):
        items = msg[len('shuffle '):].split()
        random.shuffle(items)
        return TextSendMessage('\n'.join(items))


def _echo(msg):
    prefix = '@bot '
    if msg.startswith(prefix):
        return TextSendMessage(msg[len(prefix):])


def _get_forecast_text(forecast):
    """
    天気予報の情報をテキストに変換する
    """
    date = forecast['dateLabel']
    telop = forecast['telop']
    temp = forecast['temperature']

    text = '{} は {}'.format(date, telop)
    if temp['min']:
        text += ' 最低気温{}℃'.format(temp['min']['celsius'])
    if temp['max']:
        text += ' 最高気温{}℃'.format(temp['max']['celsius'])
    return text


def _weather(msg):
    if not msg.startswith('weather'):
        return

    weather_url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city={}'
    city_code = 280010  # 神戸
    data = requests.get(weather_url.format(city_code)).json()

    text = '神戸の天気\n'
    text += _get_forecast_text(data['forecasts'][0]) + '\n'
    text += _get_forecast_text(data['forecasts'][1])
    return TextSendMessage(text)


def _fetch_yahoo_news_entry():
    url = 'http://rss.dailynews.yahoo.co.jp/fc/rss.xml'
    data = feedparser.parse(url)
    # Carousel template is accepted until 5 columns.
    # See https://devdocs.line.me/ja/#template-message
    return data['entries'][:5]


def _today_news(msg):
    if not msg.startswith('news'):
        return

    columns = [
        CarouselColumn(
            text=entry['title'],
            actions=[URITemplateAction(label='Open in Browser', uri=entry['link'])]
        )
        for entry in _fetch_yahoo_news_entry()
    ]

    carousel_template_message = TemplateSendMessage(
        alt_text="今日のニュース\nこのメッセージが見えている端末ではこの機能に対応していません。",
        template=CarouselTemplate(columns=columns)
    )
    return carousel_template_message


plugins = [_greet, _echo, _choice, _shuffle, _weather, _today_news]


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    for plugin in plugins:
        send_message = plugin(event.message.text)
        if send_message:
            line_bot_api.reply_message(event.reply_token, messages=send_message)
