from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from routes.login import db_dependency
from jose import jwt
from routes.login import SECRET_KEYS, ALGORITHM
from pydantic import BaseModel
from models.models import Comments

comment = APIRouter()
templating = Jinja2Templates(directory="templates")

class COMMENTBASE(BaseModel):
    comment :str
    user:str
    url:str


@comment.post("/comment", response_class=HTMLResponse)
async def comment_store(request:Request, db:db_dependency, url:str=Form(...), comment:str=Form(...)):
    token = request.cookies.get("access_token")
    decode= jwt.decode(token, SECRET_KEYS, algorithms=[ALGORITHM])
    user = decode['user']

    post_py = COMMENTBASE(comment=comment, user=user, url=url)
    post_db= Comments(url=post_py.url, user=post_py.user, comment=post_py.comment)
    db.add(post_db)
    db.commit()
    return RedirectResponse("/watch_Vid", status_code=303)

    