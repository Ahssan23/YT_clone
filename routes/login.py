from fastapi import APIRouter, Request, Form,Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db.db import session,Base,engine
from pydantic import BaseModel
# from jose import jwt 
from typing import Annotated
from models.models import Users
from passlib.hash import pbkdf2_sha256
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
import datetime
from jose import jwt

from jose.exceptions import JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
import os

SECRET_KEYS = "bornwithoutvvalue"
ALGORITHM = "HS256"




login = APIRouter()
template = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


class USERBASE(BaseModel):
    username:str
    password:str

    class Config :
        orm=True



def get_db():
    db= session()
    try :
        yield db

    finally : 
        db.close()
db_dependency = Annotated[session, Depends(get_db)]

def create_access_token(data: dict, expire_delta: timedelta = timedelta(minutes=60)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEYS, algorithm=ALGORITHM)
    return token



@login.get("/signup" , response_class=HTMLResponse)
async def signup_get(request:Request):
    return template.TemplateResponse("signup.html", {"request" :request})

@login.post("/signup", response_class=HTMLResponse)
async def signup(request:Request, db :db_dependency, username: str=Form(...), password:str=Form(...)):
    if_exists = db.query(Users).filter_by(username=username).first()
    if if_exists :
        print("usename already exists")
        return template.TemplateResponse("signup.html", {"request" : request, "exists" : if_exists})
    
    else :
        hashed_pass = pbkdf2_sha256.hash(password)
        print(hashed_pass)
        post_model = USERBASE(username=username ,password=hashed_pass)
        post_db = Users(username=post_model.username, password=post_model.password)
        db.add(post_db)
        db.commit()

        return RedirectResponse("/login", status_code=303)
    



#   LOGIN 

@login.get("/login" , response_class=HTMLResponse)
async def login_get(request:Request):
    return template.TemplateResponse("login.html", {"request" :request})


@login.post("/login")
async def login_post(response:Response, request:Request ,db:db_dependency,username:str=Form(...), password:str=Form(...)):
    try:
        user = db.query(Users).filter_by(username=username).first()

        if not user:
            return {"error": "Username not found"}

        if not pbkdf2_sha256.verify(password, user.password):
            return {"error": "Incorrect password"}

        data = {"user": username}
        token = create_access_token(data)
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600
        )
        return response

    except Exception as e:
        return {"error": str(e)}

