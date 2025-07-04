from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.models import Subs
from routes.login import db_dependency
from pydantic import BaseModel
from jose import jwt
from routes.login import SECRET_KEYS, ALGORITHM



subs = APIRouter()


class SUBBASE(BaseModel):
    user: str
    subbed :str

@subs.post("/subscribe", response_class=HTMLResponse)
async def sub(request:Request, db:db_dependency, user_subbed:str=Form(...) ):
    token = request.cookies.get("access_token")
    decoded_token = jwt.decode(token, SECRET_KEYS, algorithms=[ALGORITHM])
    username = decoded_token["user"]
    if username == user_subbed:
        print("can't subscribe to yourself")
        return RedirectResponse("/", status_code=303)


    else: 
        post_to_py = SUBBASE(user=username , subbed=user_subbed)
        post_db = Subs(subscriber=post_to_py.user, subbed=post_to_py.subbed)
        db.add(post_db)
        db.commit()
        
        return RedirectResponse("/", status_code=303)



