from datetime import datetime
from threading import Thread
import requests
import os
from user_agents import parse  # pyright: ignore[reportMissingImports]
from .utils import send_telegram_alert


IPINFO_TOKEN = "7facfb4cb1a3e5"


class VisitorAlertMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith(('/static/', '/media/', '/download/')) or request.path == '/favicon.ico':
            return self.get_response(request)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        path = request.path
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hostname = request.META.get('HTTP_HOST', 'Unknown')

        ua_string = request.META.get('HTTP_USER_AGENT', '')
        ua = parse(ua_string)

        device = f"{ua.device.brand or ''} {ua.device.model or ''}".strip()
        device_info = f"{device if device else 'PC'} | {ua.browser.family} on {ua.os.family}"

        def send_alert():
            try:
                res = requests.get(
                    f"https://api.ipinfo.io/lite/{ip}?token={IPINFO_TOKEN}",
                    timeout=5
                )
                data = res.json()

                country = data.get("country", "Unknown")
                city = data.get("city", "Unknown")
                isp = data.get("org", "Unknown")
                asn = data.get("asn", {}).get("asn", "Unknown")
                company = data.get("company", {}).get("name", "Unknown")

            except Exception:
                country = city = isp = asn = company = "Unknown"

            message = (
                f"🚨 Visitor Alert!\n"
                f"IP: {ip}\n"
                f"Page: {path}\n"
                f"Device: {device_info}\n"
                f"Time: {time}\n"
                f"Country: {country}\n"
                f"City: {city}\n"
                f"ISP: {isp}\n"
                f"ASN: {asn}\n"
                f"Company: {company}\n"
                f"Hostname: {hostname}"
            )

            send_telegram_alert(message)

        Thread(target=send_alert, daemon=True).start()

        return self.get_response(request)
