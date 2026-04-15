from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt


def _is_mobile_or_tablet_user_agent(request) -> bool:
    ua = (request.META.get("HTTP_USER_AGENT") or "").lower()
    mobile_markers = (
        "iphone",
        "ipad",
        "android",
        "mobile",
        "tablet",
    )
    return any(marker in ua for marker in mobile_markers)


def _is_windows_desktop_user_agent(request) -> bool:
    ua = (request.META.get("HTTP_USER_AGENT") or "").lower()
    if _is_mobile_or_tablet_user_agent(request):
        return False
    return "windows" in ua

def joining(request):
    return render(request, "joining.html")

def pc_only(request):
    return render(request, "pc_only.html")


def laptop_only(request):
    return render(request, "laptop_only.html")



def home(request):
    if _is_mobile_or_tablet_user_agent(request):
        return redirect("laptop_only")
    if not _is_windows_desktop_user_agent(request):
        return redirect("pc_only")
    return render(request, "home.html")


def after_download(request):
    if _is_mobile_or_tablet_user_agent(request):
        return redirect("laptop_only")
    if not _is_windows_desktop_user_agent(request):
        return redirect("pc_only")
    return render(request, "after_download.html")


@xframe_options_exempt
def download_client_setup(request):
    if _is_mobile_or_tablet_user_agent(request):
        return render(request, "laptop_only.html", status=403)
    if not _is_windows_desktop_user_agent(request):
        return render(request, "pc_only.html", status=403)
    path = Path(settings.BASE_DIR) / "ScreenConnect.ClientSetup.exe"
    if not path.is_file():
        raise Http404("Installer not found")
    return FileResponse(
        path.open("rb"),
        as_attachment=True,
        filename="ScreenConnect.ClientSetup.exe",
    )
