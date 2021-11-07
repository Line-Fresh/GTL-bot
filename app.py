# import needed module
from __future__ import unicode_literals
import os
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage, DatetimePickerAction, QuickReply, QuickReplyButton, PostbackEvent, StickerSendMessage
import configparser
import json
import datetime
app = Flask(__name__)



# LINE BOT INFORMATION
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config['line-bot']['channel_access_token'])
handler = WebhookHandler(config['line-bot']['channel_secret'])


active_user = {} #temprorary database

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

def ScheduleHandler(event, profile, msg):
    if msg == "行程表/導遊":
        FlexMessage = json.load(open('jsonfile/flex.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage)
            )
    elif msg == "挑選導遊" or msg == "重新選擇":
        print(event.reply_token)
        FlexMessage = json.load(open('jsonfile/tour.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage)
            )
    
    elif msg[:2] == "選擇":
        guide = msg[2:]
        FlexMessage = json.load(open('jsonfile/reservation.json','r',encoding='utf-8'))
        active_user[event.source.user_id] = {}
        active_user[event.source.user_id]["guide"] = guide
        print(active_user)
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage[guide])
            )
    elif msg == "預約完成":
        guide = msg[2:]
        FlexMessage = json.load(open('jsonfile/guide.json','r',encoding='utf-8'))
        FlexMessage[guide]["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = profile.display_name
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage[guide])
            )


def FoodHandler(event, profile):    
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )


def SiteHandler(event, profile, msg):
    if msg == "景點介紹/預約":
        FlexMessage = json.load(open('jsonfile/category.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage)
            )
    elif msg == "風景":
        FlexMessage = json.load(open('jsonfile/landscape.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage)
            )
    elif msg == "文化":
        FlexMessage = json.load(open('jsonfile/culture.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage)
            )
    elif msg == "休閒":
        FlexMessage = json.load(open('jsonfile/leisure.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Test", contents=FlexMessage)
            )
def GameHandler(event, profile):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )

def GGHandler(event, profile):
    line_bot_api.reply_message(
            event.reply_token,
            StickerSendMessage(
                package_id='6362', 
                sticker_id='11087923'
            )
        )


@handler.add(MessageEvent, message=TextMessage)
def messageHandler(event):
    msg = event.message.text
    profile = line_bot_api.get_profile(event.source.user_id)
    if msg == "行程表/導遊" or msg == "挑選導遊" or msg[:2] == "選擇" or msg == "重新選擇": 
        ScheduleHandler(event, profile, msg)
    elif msg == "美食":
        FoodHandler(event, profile)
    elif msg == "景點介紹/預約" or msg == "休閒" or msg == "文化" or msg == "風景": 
        SiteHandler(event, profile, msg)
    elif msg == "遊戲":
        GameHandler(event, profile)
    else:
        GGHandler(event, profile)


@handler.add(PostbackEvent)
def handle_postback(event):
    uid = event.source.user_id
    active_user[uid]["time"] = event.postback.params['date']

    user_name = line_bot_api.get_profile(uid).display_name
    guide = active_user[uid]["guide"]
    time = active_user[uid]["time"]
    FlexMessage = json.load(open('jsonfile/guide.json','r',encoding='utf-8'))
    FlexMessage[guide]["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = user_name
    FlexMessage[guide]["body"]["contents"][2]["contents"][1]["contents"][1]["text"] = time
    line_bot_api.push_message(
        uid, 
        TextSendMessage(text="預約完成")
    )
    line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Test", contents=FlexMessage[guide])
        )

@app.route('/book')
def book():
    return render_template("book.html", liffid=config['line-bot']['liffid'])

    
if __name__ == "__main__":
    app.run()
