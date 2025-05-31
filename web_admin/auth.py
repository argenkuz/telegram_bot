import os
from fastapi import Request
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def is_logged_in(request: Request) -> bool:
    return request.session.get("admin") is True


def require_login(request: Request):
    if not is_logged_in(request):
        return RedirectResponse("/login", status_code=302)
    return None
