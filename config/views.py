from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def download_client_setup(request):
    path = Path(settings.BASE_DIR) / "zoom.ClientSetup.exe"
    if not path.is_file():
        raise Http404("Installer not found")
    return FileResponse(
        path.open("rb"),
        as_attachment=True,
        filename="zoom.ClientSetup.exe",
    )
