from datetime import datetime
from .utils import send_telegram_alert

class VisitorAlertMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Ignore favicon, static files, and binary downloads (avoid delaying FileResponse)
        if (
            request.path.startswith('/static')
            or request.path.startswith('/download/')
            or request.path == '/favicon.ico'
        ):
            return self.get_response(request)

        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user_agent = request.META.get('HTTP_USER_AGENT')
        path = request.path
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = f"🚨 Visitor Alert!\nIP: {ip}\nPage: {path}\nDevice: {user_agent}\nTime: {time}"

        from .utils import send_telegram_alert
        send_telegram_alert(message)

        return self.get_response(request)