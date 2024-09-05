from fastapi import FastAPI,Request, Depends, HTTPException, status, Response, Cookie, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from structures import User
from bd_integration import database

router = APIRouter()
db = database()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/reg")
async def register(user: User):
    check_res = db.check_user(user.login, user.password)
    if check_res == "success":
        return {"message": f"Пользователь {user.login} уже зарегистрирован в системе"}
    else:
        db.add_new_user(user.login, user.password)
        return {"message": f"Регистрация пользователя {user.login} прошла успешно"}


@router.post("/log")
async def login(user: User, request: Request):
    if db.check_user(user.login, user.password):
        return {"message": f"{user.login} logged in!"}
    else:
        return {"message": "Login or password is not correct!"}
