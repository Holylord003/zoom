import requests

BOT_TOKEN = "8730132561:AAFkTHQqx4WWrAf8y98hzN3hPSI-10Wx8tA"
CHAT_ID = "8692660371"

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)