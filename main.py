import os
import sys
import requests
from linebot.exceptions import LineBotApiError
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)
from flask import Flask, request, abort, send_file
app = Flask(__name__)

channel_secret = ''
channel_access_token = ''
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def _is_item_about_msg(msg):
    target_txt = ['あいてむ', 'アイテム', 'item']
    list_flg = [x in msg for x in target_txt]
    if any(list_flg):
        return True
    else:
        return False

def _GetStoreInfo():
    URL = 'https://api.fortnitetracker.com/v1/store'
    key = ''

    headers = {'TRN-Api-Key' : key}
    r = requests.get(URL, headers=headers)
    list_result = eval(r.text)
    return list_result

def get_item_info():
    # アイテム情報をLINEAPIに渡せる形のリスト形式で返す
    list_result_items = _GetStoreInfo()
    
    list_return_object = []
    for i, x in enumerate(list_result_items):
        if i == 5:
            break;
        imageUrl = x['imageUrl']
        img_msg = ImageSendMessage(original_content_url=imageUrl, preview_image_url=imageUrl)

        list_return_object.append(img_msg)
    return list_return_object

def main(request):
    request_json = request.get_json()
    events = request_json['events']
    reply_token = events[0]['replyToken']
    request_msg = events[0]['message']['text']
    
    body = request.get_data(as_text=True)
    signature = request.headers.get('X-Line-Signature')

    @handler.add(MessageEvent, message=TextMessage)
    def message(line_event):
        
        if _is_item_about_msg(request_msg):
            list_return_object = get_item_info()
        else:
            txt = 'アイテムしか取ってこれないの、ごめんね'
            list_return_object = TextSendMessage(text=txt)

        line_bot_api.reply_message(reply_token, list_return_object)

    handler.handle(body, signature)

    return f''

