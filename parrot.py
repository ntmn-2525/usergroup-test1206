# -*- coding: utf-8 -*-　
from flask import Flask, request, abort
import os
import argparse
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")

#感情解析API
def analyze_sentiment():
    
    # クライアントのインスタンス化
    language_client = language.Client()

    # 分析したいテキスト
    text = """
    頑張れ頑張れできるできる絶対できる頑張れもっとやれるって.
    やれる気持ちの問題だ頑張れ頑張れそこだ！
    そこで諦めるな絶対に頑張れ積極的にポジティブに頑張る頑張る.
    """

    # リクエストのデータを格納
    document = language_client.document_from_text(text)
    # 感情分析のレスポンスを格納
    response = document.analyze_sentiment()
    # ドキュメント全体の感情が含まれたオブジェクト
    sentiment = response.sentiment
    # 各段落の感情が含まれたオブジェクトのリスト
    sentences = response.sentences

    # 全体の感情スコアを出力
    return 'Text: {}'.format(text).'Sentiment: {}'.format(sentiment.score)
    #print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

    # 各段落の感情スコアを出力
    #for sentence in sentences:
    #    print('=' * 20)
    #    print('Text: {}'.format(sentence.content.encode('utf_8'))) #追加
    #    print('Sentiment: {}, {}'.format(sentence.sentiment.score, sentence.sentiment.magnitude))




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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
