# import needed module
from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import configparser
import json
app = Flask(__name__)


# LINE BOT INFORMATION
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config['line-bot']['channel_access_token'])
handler = WebhookHandler(config['line-bot']['channel_secret'])

# LINE BOT REPLY
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'Nice'

def ScheduleHandler(event, profile):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )
def FoodHandler(event, profile):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )
def SiteHandler(event, profile):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )

def GameHandler(event, profile):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )

def GGHandler(event, profile):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="You GG")
        )

@handler.add(MessageEvent, message=TextMessage)
def messageHandler(event):
    msg = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    if msg == "行程表/導遊":
        ScheduleHandler(event, profile)
    elif msg == "美食":
        FoodHandler(event, profile)
    elif msg == "景點介紹/預約":
        SiteHandler(event, profile)
    elif msg == "遊戲":
        GameHandler(event, profile)
    else:
        GGHandler(event, profile)

if __name__ == "__main__":
    app.run()
