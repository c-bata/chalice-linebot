# coding: utf-8
from __future__ import unicode_literals
from __future__ import print_function

from chalicelib import (
    app, line_bot_api, handler
)

from chalicelib import postback_events, text_message_events, aws_utils
from linebot.models import (
    MessageEvent, JoinEvent, PostbackEvent, TextMessage, TextSendMessage,
    ImageMessage
)


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
    line_bot_api.reply_message(event.reply_token, TextSendMessage(msg))


# ====================================
# Postback
# ====================================
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'leave':
        postback_events.postback_leave(event)


# ====================================
# Message Event, TextMessage
# ====================================
plugins = [
    text_message_events.greet,
    text_message_events.weather,
    text_message_events.choice,
    text_message_events.shuffle,
    text_message_events.omikuji,
    text_message_events.today_news,
    text_message_events.echo,
    text_message_events.sudden_death,
    text_message_events.wikipedia,
]


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    for plugin in plugins:
        plugin(event)


# ====================================
# Message Event, ImageMessage
# ====================================
@handler.add(MessageEvent, message=ImageMessage)
def handle_content_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    image_url = aws_utils.upload_to_s3(message_content)
    print(image_url)
