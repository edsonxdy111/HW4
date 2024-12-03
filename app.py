# -*- coding: utf-8 -*-

#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('lGJptEbFtXo8Oo/4sd8fkzLimI2S47IjUh5ucOEE1NwzpWTUc1Nj8BOYUGxRH3cGugd43Icu6kHMICp81xG/SzMItnqC8lAtpSYpLWETlZxL+eLOQfsRqtSg9EGWZbCkOl9PoE/NGrpYIjUDygJNKAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('c89e2063d758e521c1ffd9fdcab952d0')

line_bot_api.push_message('U37a9085018df3036884499a3904ff34c', TextSendMessage(text='你可以開始了'))

# 生日祝福圖片 URL
birthday_image_url = "https://png.pngtree.com/back_origin_pic/04/46/16/44225a8d1e41eceff00c0d444937081f.jpg"  # 替換為您的圖片網址

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()  # 使用者輸入的訊息

    if user_message == "今天是我的生日":
        # 傳送生日祝福圖片
        image_message = ImageSendMessage(
            original_content_url=birthday_image_url,  # 實際圖片 URL
            preview_image_url=birthday_image_url  # 預覽圖片 URL（可以與圖片 URL 相同）
        )
        text_message = TextSendMessage(text="生日快樂！🎉🎂")  # 祝福文字

        # 回傳圖片與文字訊息
        line_bot_api.reply_message(event.reply_token, [image_message, text_message])
    else:
        # 若非生日訊息，回應提示訊息
        reply_message = TextSendMessage(text="請告訴我：今天是我的生日，我將為您送上祝福！")
        line_bot_api.reply_message(event.reply_token, reply_message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)