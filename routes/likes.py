from fastapi import APIRouter,Request,Form
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from routes.login import db_dependency
from models.models import Likes
from jose import jwt
from pydantic import BaseModel
from routes.login import SECRET_KEYS, ALGORITHM


like = APIRouter()
templating = Jinja2Templates(directory="templates")

class LIKEBASE(BaseModel):
    url :str
    user :str
    class Config:
        orm: True


@like.post("/like"  , response_class=HTMLResponse)
async def like_video(request:Request, db:db_dependency, url: str=Form(...)):
    token = request.cookies.get("access_token") 
    decoded = jwt.decode(token, SECRET_KEYS, algorithms=[ALGORITHM])    
    user = decoded["user"]
    already_likes=  db.query(Likes).filter_by(url=url , user=user).all()
    get_likes = db.query(Likes).filter_by(url=url).all()
    likes = list(set([v.user for v in get_likes]))
    if already_likes :
        print("already likes")
        return templating.TemplateResponse("watch_Vid.html", {"request":request , "url": url,"likes": likes })
    else:

        post_py = LIKEBASE(url=url, user=user)
        post_db = Likes(url=post_py.url,  user=post_py.user)
        db.add(post_db)
        db.commit()
        
        return templating.TemplateResponse("watch_Vid.html", {"request":request , "url": url,"likes": likes })
    

