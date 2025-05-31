import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from database.db import async_session
from database.models import Keyword, User
from sqlalchemy import select
from datetime import datetime
from dotenv import load_dotenv
from web_admin.auth import is_logged_in, require_login, ADMIN_PASSWORD

load_dotenv()

app = FastAPI()

# Используем секрет из .env
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET"))

templates = Jinja2Templates(directory="web_admin/templates")


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        request.session["admin"] = True
        return RedirectResponse("/admin", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный пароль"})


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    redir = require_login(request)
    if redir:
        return redir

    async with async_session() as session:
        keywords = (await session.execute(select(Keyword))).scalars().all()
        users = (await session.execute(select(User))).scalars().all()
        now = datetime.utcnow()
        active_users = [u for u in users if u.trial_end > now or (u.subscription_end and u.subscription_end > now)]
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "keywords": keywords,
        "active_users": active_users,
        "users": users
    })


@app.post("/add_keyword")
async def add_keyword(request: Request, word: str = Form(...), category: str = Form(...)):
    redir = require_login(request)
    if redir:
        return redir

    async with async_session() as session:
        session.add(Keyword(word=word.lower(), category=category.lower()))
        await session.commit()
    return RedirectResponse("/admin", status_code=302)


@app.post("/delete_keyword")
async def delete_keyword(request: Request, word_id: int = Form(...)):
    redir = require_login(request)
    if redir:
        return redir

    async with async_session() as session:
        keyword = await session.get(Keyword, word_id)
        if keyword:
            await session.delete(keyword)
            await session.commit()
    return RedirectResponse("/admin", status_code=302)
