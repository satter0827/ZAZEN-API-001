from flask import Flask, request, abort, make_response
from gtts import gTTS
import os, requests, json, pychromecast

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

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route('/')
def hello():
    name = "Hello World"
    return name

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

@app.route("/mp3/<string:file_name>", methods=['GET'])
def getMP3File(file_name):
    response = make_response()

    if not os.path.exists(file_name):
        return response

    response.data = open(file_name, "rb").read()
    response.headers['Content-Disposition'] = 'attachment; filename=' + file_name 
    response.mimetype = 'audio/mp3'
    return response

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if (event.message.text == "座禅を開始して"):
        hento = "座禅を始めます"

        WEB_HOOK_OBNIZ = "https://obniz.com/events/1512/BTca5D9lB2kHYP8nrqbapur3JIlw6fpR/run"
        requests.post(WEB_HOOK_OBNIZ)

        WEB_HOOK_GOOGLE = "https://c40e66b6eaee.ngrok.io/mp3/start"
        requests.get(WEB_HOOK_GOOGLE)

    elif (event.message.text == "座禅を終了して"):
        hento = "座禅を終わります"

        WEB_HOOK_GOOGLE = "https://obniz.com/events/1512/BTca5D9lB2kHYP8nrqbapur3JIlw6fpR/run"
        requests.get(WEB_HOOK_GOOGLE)

        WEB_HOOK_GOOGLE = "https://c40e66b6eaee.ngrok.io/mp3/start"
        requests.get(WEB_HOOK_GOOGLE)

    elif (event.message.text == "喝を入れて"):
        hento = "喝!!!"

        WEB_HOOK_GOOGLE = "https://obniz.com/events/1512/BTca5D9lB2kHYP8nrqbapur3JIlw6fpR/run"
        requests.get(WEB_HOOK_GOOGLE)

        WEB_HOOK_GOOGLE = "https://c40e66b6eaee.ngrok.io/mp3/start"
        requests.get(WEB_HOOK_GOOGLE)

    else:
        hento = event.message.text

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=hento))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)