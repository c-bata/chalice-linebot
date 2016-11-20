from linebot.models import TextSendMessage, SourceGroup, SourceRoom
from . import line_bot_api


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
