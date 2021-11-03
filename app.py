# 載入需要的模組
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


def isGreeting(msg):
    greeting = ["hello", "hi", "哈囉", "嗨", "海螺"]
    flag = False
    for m in greeting:
        if msg.lower() in m or m in msg.lower():
            flag = True
    return flag

@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    msg = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    if isGreeting(msg):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )

if __name__ == "__main__":
    app.run()
