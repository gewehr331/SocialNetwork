import httpx
from fastapi import FastAPI, Request, HTTPException, status, Depends, Response, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import aiofiles
from bd_integration import database
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse
import requests
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()
db = database()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class User(BaseModel):
    login: str
    password: str


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/register", response_class=HTMLResponse)
async def registration():
    async with aiofiles.open("templates/register.html", mode="r", encoding="utf-8") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")


@app.get("/login", response_class=HTMLResponse)
async def login_page():
    async with aiofiles.open("templates/login.html", mode="r", encoding="utf-8") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content, media_type="text/html; charset=utf-8")


@app.post("/register")
async def register(user: User):
    check_res = db.check_user(user.login, user.password)
    if check_res == "success":
        return {"message": f"Пользователь {user.login} уже зарегистрирован в системе"}
    else: 
        db.add_new_user(user.login, user.password)
        return {"message": f"Регистрация пользователя {user.login} прошла успешно"}


@app.post("/login")
async def login(user: User, request: Request):
    if db.check_user(user.login, user.password):
        return {"message": f"{user.login} logged in!"}
    else:
        return {"message": "Login or password is not correct!"}


@app.get("/profile", response_class=HTMLResponse)
async def profile(login_name: str, request: Request):
    return templates.TemplateResponse("profile.html", {"request": request, "login": login_name})


@app.options("/login")
async def options_login():
    return {"Allow": "POST, OPTIONS, GET"}


@app.options("/register")
async def options_register():
    return {"Allow": "POST, OPTIONS, GET"}


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

