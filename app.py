# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

import re
import random

from bs4 import BeautifulSoup
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


def _fetch_news():
    # RSS Feed of yahoo news doesn't contain thumbnail image.
    url = 'https://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&topic=po&output=rss'
    parsed = feedparser.parse(url)
    # Carousel template is accepted until 5 columns.
    # See https://devdocs.line.me/ja/#template-message
    return parsed.entries[:5]


def _get_carousel_column_from_google_news_entry(entry):
    summary_soup = BeautifulSoup(entry.summary, "html.parser")
    # summary has img tag which has no src attribute like:
    # <img alt="" height="1" width="1"/>
    images = [x for x in summary_soup.find_all('img') if x.has_attr('src')]
    if len(images) == 0:
        return
    thumbnail_url = images[0]['src']

    # carousel column text is accepted until 60 characters when set the thumbnail image.
    carousel_text = summary_soup.find_all('font')[5].contents[0]
    carousel_text = carousel_text[:57] + '...' if len(carousel_text) > 60 else carousel_text

    # carousel column title is accepted until 40 characters.
    title = entry.title[:37] + '...' if len(entry.title) > 40 else entry.title

    return CarouselColumn(
        thumbnail_image_url=thumbnail_url,
        title=title,
        text=carousel_text,
        actions=[URITemplateAction(label='Open in Browser', uri=entry.link)],
    )


def _today_news(msg):
    if not msg.startswith('news'):
        return

    columns = [_get_carousel_column_from_google_news_entry(entry) for entry in _fetch_news()]
    columns = [c for c in columns if c is not None]

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
