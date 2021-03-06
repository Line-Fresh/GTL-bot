# import needed module
from __future__ import unicode_literals
import os
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, FlexSendMessage, DatetimePickerAction, QuickReply, QuickReplyButton, PostbackEvent, StickerSendMessage
import configparser
import json
import random
import datetime
app = Flask(__name__)


# LINE BOT INFORMATION
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config['line-bot']['channel_access_token'])
handler = WebhookHandler(config['line-bot']['channel_secret'])


active_user = {} #temprorary database
travel_url = ["https://travel.line.me/r/xCdiGGc1V6", "https://travel.line.me/r/HSnQGmNqHk"] #line travel url
appear = [False]*5 # for random 

def bugfixer(uid):
    if uid not in active_user:
        active_user[uid] = {"guide" : "Johnson", "time" : "預計旅遊時間：3小時", "transportation" : "預計交通工具：步行", "type" : "預計旅行類別：自然", "degree" : "預計旅行方式：虎尾輕旅行"}
    else:
        if "guide" not in active_user[uid]:
            active_user[uid]["guide"] = "Johnson"
        if "time" not in active_user[uid]:
            active_user[uid]["time"] = "預計旅遊時間：9小時"
        if "transportation" not in active_user[uid]:
            active_user[uid]["transportation"] = "預計交通工具：步行"
        if "type" not in active_user[uid]:
            active_user[uid]["type"] = "預計旅行類別：自然"
        if "degree" not in active_user[uid]:
            active_user[uid]["degree"] = "預計旅行方式：虎尾輕旅行"
    return
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
        FlexMessage = json.load(open('jsonfile/schedule/flex.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            )
    elif msg == "挑選導遊" or msg == "重新選擇":
        print(event.reply_token)
        FlexMessage = json.load(open('jsonfile/schedule/tour.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            )
    
    elif msg[:2] == "選擇":
        uid = event.source.user_id
        guide = msg[2:]
        FlexMessage = json.load(open('jsonfile/schedule/reservation.json','r',encoding='utf-8'))
        bugfixer(uid)
        active_user[uid]["guide"] = guide
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage[guide])
            )
    elif msg == "預約完成":
        guide = msg[2:]
        FlexMessage = json.load(open('jsonfile/schedule/guide.json','r',encoding='utf-8'))
        FlexMessage[guide]["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = profile.display_name
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage[guide])
            )
    elif msg == "開始安排行程":
        uid = event.source.user_id
        FlexMessage = json.load(open('jsonfile/schedule/time.json','r',encoding='utf-8'))
        bugfixer(uid)
        line_bot_api.push_message(
            uid, 
            TextSendMessage(text="預計旅遊時間")
        )
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            )
    elif msg[:6] == "預計旅程時間":
        uid = event.source.user_id
        FlexMessage = json.load(open('jsonfile/schedule/transportation.json','r',encoding='utf-8'))
        line_bot_api.push_message(
            uid, 
            TextSendMessage(text="預計交通工具")
        )
        bugfixer(uid)
        active_user[uid]["time"] = msg
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            ) 
    elif msg[:6] == "預計交通工具":
        uid = event.source.user_id
        FlexMessage = json.load(open('jsonfile/schedule/type.json','r',encoding='utf-8'))
        line_bot_api.push_message(
            uid, 
            TextSendMessage(text="預計旅行類別")
        )
        bugfixer(uid)
        active_user[uid]["transportation"] = msg
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            ) 
    elif msg[:6] == "預計旅行類別":
        uid = event.source.user_id
        bugfixer(uid)
        active_user[uid]["type"] = msg
        user = active_user[uid]
        line = "======================="
        url = travel_url[random.randint(0, 1)]
        url = f'參考行程：{url}'
        result = f'生成結果\n{line}\n{user["time"]}\n{user["transportation"]}\n{user["type"]}\n{url}'
        line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=result)
            ) 
def FoodHandler(event, profile):    
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hello " + profile.display_name[1:])
        )


def SiteHandler(event, profile, msg):
    if msg == "景點介紹/預約":
        FlexMessage = json.load(open('jsonfile/site/category2.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            )
    elif msg == "風景":
        FlexMessage = json.load(open('jsonfile/site/landscape.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            )
    elif msg == "文化":
        FlexMessage = json.load(open('jsonfile/site/culture.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            )
    elif msg == "休閒":
        FlexMessage = json.load(open('jsonfile/site/leisure.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
            )


def SocialHandler(event, profile, msg):
    if msg == "社交":
        FlexMessage = json.load(open('jsonfile/social/social_opening.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
        )
    elif msg == "社交：美食":
        FlexMessage = json.load(open('jsonfile/social/group1.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
        )
    elif msg == "社交：遊戲":
        FlexMessage = json.load(open('jsonfile/social/group1.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
        )
    elif msg == "社交：寵物":
        FlexMessage = json.load(open('jsonfile/social/group1.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
        )
    elif msg == "社交：事業":
        FlexMessage = json.load(open('jsonfile/social/group1.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
        )
    elif msg == "隨機生成":
        num = random.randint(2, 4)
        while appear[num]:
            num = random.randint(2, 4)
        appear[num] = True
        FlexMessage = json.load(open(f'jsonfile/social/group{num}.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
        )

def GameHandler(event, profile, msg):
    if msg == "遊戲":
        FlexMessage = json.load(open('jsonfile/game/games.json','r',encoding='utf-8'))
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage)
        )
    # should have a db to save the details of the game
    elif msg == "闖關遊戲":
        f = open("./textfile/normal_game.txt", "r")
        message = f.read()
        f.close()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    elif msg[:4] == "即時競賽":
        f = open("./textfile/special_game/train.txt", "r")
        message = f.read()
        f.close()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
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
    if msg == "行程表/導遊" or msg == "挑選導遊" or msg[:2] == "選擇" or msg == "重新選擇" or msg == "開始安排行程" or msg[:6] == "預計旅程時間" or msg[:6] == "預計交通工具" or msg[:6] == "預計旅行類別" or msg[:6] == "預計旅行方式":
        ScheduleHandler(event, profile, msg)
    elif msg == "美食":
        FoodHandler(event, profile)
    elif msg == "景點介紹/預約" or msg == "休閒" or msg == "文化" or msg == "風景" or msg[:4] == "預約成功": 
        SiteHandler(event, profile, msg)
    elif msg == "遊戲" or msg == "闖關遊戲" or msg[:4] == "即時競賽":
        GameHandler(event, profile, msg)
    elif msg == "社交" or msg == "社交：美食" or msg == "社交：遊戲" or msg == "社交：寵物" or msg == "社交：事業" or msg == "隨機生成":
        SocialHandler(event, profile, msg)
    else:
        GGHandler(event, profile)


@handler.add(PostbackEvent)
def handle_postback(event):
    uid = event.source.user_id
    bugfixer(uid)
    active_user[uid]["time"] = event.postback.params['date']

    user_name = line_bot_api.get_profile(uid).display_name
    guide = active_user[uid]["guide"]
    time = active_user[uid]["time"]
    FlexMessage = json.load(open('jsonfile/schedule/guide.json','r',encoding='utf-8'))
    FlexMessage[guide]["body"]["contents"][2]["contents"][0]["contents"][1]["text"] = user_name
    FlexMessage[guide]["body"]["contents"][2]["contents"][1]["contents"][1]["text"] = time
    line_bot_api.push_message(
        uid, 
        TextSendMessage(text="預約完成")
    )
    line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="Green Thunder Legend", contents=FlexMessage[guide])
        )

@app.route('/book')
def book():
    return render_template("book.html", liffid=config['line-bot']['book_liffid'])


@app.route('/social')
def social():
    return render_template("social.html", liffid=config['line-bot']['social_liffid'])

    
if __name__ == "__main__":
    app.run()
