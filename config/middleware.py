from datetime import datetime
from .utils import send_telegram_alert
import requests

class VisitorAlertMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user_agent = request.META.get('HTTP_USER_AGENT')
        path = request.path
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = geo.get("country", "Unknown")
        site_url = "zoom link"

        message = f"🚨 Zoom Visitor Alert!\nIP: {ip}\nPage: {path}\nDevice: {user_agent}\nTime: {time}\nCountry: {country}\nSite URL: {site_url}"

        send_telegram_alert(message)

        response = self.get_response(request)
        return response