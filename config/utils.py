import requests

BOT_TOKEN = "8650659778:AAFQBS2_wZcUfYZYhuDJnTdz2o6wOw4S7Rc"
CHAT_ID = "1635116489"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)