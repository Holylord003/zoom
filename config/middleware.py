from datetime import datetime
from threading import Thread
from .utils import send_telegram_alert


class VisitorAlertMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Ignore static/media/download files
        if request.path.startswith(('/static/', '/media/', '/download/')) or request.path == '/favicon.ico':
            return self.get_response(request)

        # Get IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        path = request.path
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        country = request.META.get('HTTP_CF_IPCOUNTRY', 'Unknown')
        city = request.META.get('HTTP_CF_CITY', 'Unknown')
        isp = request.META.get('HTTP_CF_ISP', 'Unknown')
        hostname = request.META.get('HTTP_HOST', 'Unknown')

        message = (
            f"🚨 Visitor Alert!\n"
            f"IP: {ip}\n"
            f"Page: {path}\n"
            f"Device: {user_agent}\n"
            f"Time: {time}\n"
            f"Country: {country}\n"
            f"City: {city}\n"
            f"ISP: {isp}\n"
            f"Hostname: {hostname}"
        )

        # Send Telegram alert in background thread
        Thread(target=send_telegram_alert, args=(message,)).start()

        return self.get_response(request)