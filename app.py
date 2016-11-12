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
    MessageEvent, JoinEvent, PostbackEvent,
    TextMessage, TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
    SourceGroup, SourceRoom,
)
import requests
from unicodedata import east_asian_width

app = Chalice(app_name='linebot')
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_ACCESS_SECRET')

HELP_TEXT = """
Reply:
  @bot ping
  @bot bye
  @bot hey

Commands:
  おはよう, 眠い...
  choice A B
  shuffle A B
  おみくじ or 今日の運勢
  weather
  news
  突然の死
  突然の死 カレーメシ
"""[1:-1]


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


# ====================================
# Join
# ====================================
@handler.add(JoinEvent)
def handle_join(event):
    msg = 'Joined this {}!\nみなさん、よろしくお願いします :)'.format(event.source.type)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))


# ====================================
# Postback
# ====================================
def postback_leave(event):
    if isinstance(event.source, SourceGroup):
        line_bot_api.reply_message(event.reply_token,
                                   messages=TextSendMessage('Leaving group'))
        line_bot_api.leave_group(event.source.group_id)
    elif isinstance(event.source, SourceRoom):
        line_bot_api.reply_message(event.reply_token,
                                   messages=TextSendMessage('Leaving room'))
        line_bot_api.leave_group(event.source.room_id)
    else:
        line_bot_api.reply_message(event.reply_token,
                                   messages=TextSendMessage("Bot can't leave from 1:1 chat"))


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'leave':
        postback_leave(event)


# ====================================
# Weather
# ====================================
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


def weather(event):
    msg = event.message.text
    if not msg.startswith('weather'):
        return

    weather_url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city={}'
    city_code = 280010  # 神戸
    data = requests.get(weather_url.format(city_code)).json()

    text = '神戸の天気\n'
    text += _get_forecast_text(data['forecasts'][0]) + '\n'
    text += _get_forecast_text(data['forecasts'][1])
    line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(text))


# ====================================
# Greeting
# ====================================
def greet(event):
    msg = event.message.text
    greetings = [
        ('ぽやしみ|おやすみ|眠た?い|ねむた?い|寝る|寝ます', ['おやすみー', 'おやすみなさい']),
        ('いってきま|行ってきま', ['いってらっしゃい', 'いってら']),
        ('こんにち[はわ]', ['こんにちは', 'こんにちは、元気ですかー?']),
        ('おはよう|お早う', ['おはよー', 'おはよう', 'おはようございます！']),
        ('疲れた|つかれた', ['おつかれー', 'おつかれ！', 'お疲れ様！']),
    ]
    for pattern, replies in greetings:
        if re.match(pattern, msg):
            line_bot_api.reply_message(event.reply_token,
                                       messages=TextSendMessage(random.choice(replies)))
            return


# ====================================
# Choice, Shuffle, おみくじ
# ====================================
def choice(event):
    msg = event.message.text
    if not re.match('^[cC]hoice.*', msg):
        return
    items = msg[len('choice '):].split()
    line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(random.choice(items)))


def shuffle(event):
    msg = event.message.text
    if not re.match('^[sS]huffle.*', msg):
        return
    items = msg[len('shuffle '):].split()
    random.shuffle(items)
    line_bot_api.reply_message(event.reply_token, messages=TextSendMessage('\n'.join(items)))


def omikuji(event):
    msg = event.message.text
    if not re.match('おみくじ|今日の運勢', msg):
        return
    fortunes = ['大吉', '中吉', '吉', '末吉', '凶', '大凶']
    line_bot_api.reply_message(event.reply_token,
                               messages=TextSendMessage(random.choice(fortunes)))


# ====================================
# NEWS
# ====================================
def _fetch_news():
    # RSS Feed of yahoo news doesn't contain thumbnail image.
    url = 'https://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&topic=po&output=rss'
    parsed = feedparser.parse(url)
    return parsed.entries


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


def today_news(event):
    msg = event.message.text
    if not msg.startswith('news'):
        return

    columns = [_get_carousel_column_from_google_news_entry(entry) for entry in _fetch_news()]
    # Carousel template is accepted until 5 columns.
    # See https://devdocs.line.me/ja/#template-message
    columns = [c for c in columns if c is not None][:5]

    carousel_template_message = TemplateSendMessage(
        alt_text="今日のニュース\nこのメッセージが見えている端末ではこの機能に対応していません。",
        template=CarouselTemplate(columns=columns)
    )
    line_bot_api.reply_message(event.reply_token, messages=carousel_template_message)


# ====================================
# Echo
# ====================================
def _leave(event):
    confirm_template_message = TemplateSendMessage(
        alt_text='Are you sure?',
        template=ConfirmTemplate(
            text='Are you sure?',
            actions=[
                PostbackTemplateAction(label='Yes', text='Yes', data='leave'),
                MessageTemplateAction(label='No', text='No')
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, messages=confirm_template_message)


def echo(event):
    msg = event.message.text
    prefix = '@bot '
    if not msg.startswith(prefix):
        return
    msg = msg[len(prefix):]

    if msg.startswith('ping'):
        line_bot_api.reply_message(event.reply_token, messages=TextSendMessage('pong'))
    elif re.match('[Bb]ye', msg):
        _leave(event)
    elif re.match('[hH]ey.*', msg):
        profile = line_bot_api.get_profile(event.source.user_id)
        msg = 'Hey {}!'.format(profile.display_name)
        line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(msg))
    elif re.match('help|ヘルプ', msg):
        line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(HELP_TEXT))
    else:
        msg = "Sorry, I don't understand your command :(\nPlease input '@bot help'"
        line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(msg))


# ====================================
# Sudden death
# ====================================
def _message_length(message):
    """ メッセージの長さを返す """
    length = 0
    for char in message:
        width = east_asian_width(char)
        if width in ('W', 'F', 'A'):
            length += 2
        elif width in ('Na', 'H'):
            length += 1
    return length


def sudden_death(event):
    """ 突然の死のメッセージを返す """
    msg = event.message.text
    if not re.match('^突然の死.*', msg):
        return

    word = msg[len('突然の死'):].lstrip().rstrip()
    word = word if word else '突然の死'
    length = _message_length(word)
    header = '＿' + '人' * (length // 2 + 2) + '＿'
    footer = '￣' + 'Y^' * (length // 2) + 'Y￣'
    middle = "＞　" + word + "　＜"

    msg = "\n".join([header, middle, footer])
    line_bot_api.reply_message(event.reply_token, messages=TextSendMessage(msg))


# ====================================
# Message Event, TextMessage
# ====================================
plugins = [greet, weather, choice, shuffle, omikuji, today_news, echo, sudden_death]


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    for plugin in plugins:
        plugin(event)
