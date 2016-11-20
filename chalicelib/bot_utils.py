# coding: utf-8
from __future__ import unicode_literals
import feedparser
import requests
from unicodedata import east_asian_width
import wikipedia


# ====================================
# Sudden death
# ====================================
def _message_length(word):
    """Return a message length."""
    length = 0
    for char in word:
        width = east_asian_width(char)
        if width in ('W', 'F', 'A'):
            length += 2
        elif width in ('Na', 'H'):
            length += 1
    return length


def sudden_death(word):
    """Return a decorated message."""
    length = _message_length(word)
    return "\n".join([
        '＿' + '人' * (length // 2 + 2) + '＿',
        "＞  " + word + "  ＜",
        '￣' + 'Y^' * (length // 2) + 'Y￣'
    ])


# ====================================
# Wikipedia
# ====================================
def wikipedia_search(word):
    """Search a word meaning on wikipedia."""
    wikipedia.set_lang('ja')
    results = wikipedia.search(word)

    # get first result
    if results:
        page = wikipedia.page(results[0])
        msg = page.title + "\n" + page.url
    else:
        msg = '`{}` に該当するページはありません'.format(word)
    return msg


# ====================================
# Google News
# ====================================
def google_news():
    # RSS Feed of yahoo news doesn't contain thumbnail image.
    url = 'https://news.google.com/news?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&topic=po&output=rss'
    parsed = feedparser.parse(url)
    return parsed.entries


# ====================================
# Weather
# ====================================
def _generate_forecast_text(forecast):
    """Generate a forecast from livedoor weather's text"""
    date = forecast['dateLabel']
    telop = forecast['telop']
    temp = forecast['temperature']

    text = '{} は {}'.format(date, telop)
    if temp['min']:
        text += ' 最低気温{}℃'.format(temp['min']['celsius'])
    if temp['max']:
        text += ' 最高気温{}℃'.format(temp['max']['celsius'])
    return text


def livedoor_forecast():
    weather_url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city={}'
    city_code = 280010  # 神戸
    data = requests.get(weather_url.format(city_code)).json()

    text = '\n'.join([
        '神戸の天気',
        _generate_forecast_text(data['forecasts'][0]),
        _generate_forecast_text(data['forecasts'][1]),
    ])
    return text
