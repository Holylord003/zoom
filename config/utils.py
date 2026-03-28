import requests

BOT_TOKEN = "8731118171:AAFaeVLOvy4HPbLhg12MdnMLFxxVi5Fd8u4"
CHAT_ID = "8330440211"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)