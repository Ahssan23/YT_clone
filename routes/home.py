from fastapi import APIRouter,Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routes.login import db_dependency
from models.models import Video, Subs, Likes,Comments  
from jose import jwt
from routes.login import SECRET_KEYS, ALGORITHM

home = APIRouter()
templating = Jinja2Templates(directory="templates")




@home.get("/", response_class=HTMLResponse)
async def home_get(request:Request, db:db_dependency):
    token = request.cookies.get("access_token")
    decoded =  jwt.decode(token, SECRET_KEYS, algorithms=[ALGORITHM])
    user = decoded["user"]
    get_url = db.query(Video).filter().all()
    urls = list([(v.url,v.user, v.title) for v in get_url])


    get_subs = db.query(Subs).filter_by(subscriber=user).all()
    count = list([v.subbed for v in get_subs])

    get_likes = db.query(Likes).filter().all()
    likes = list(set([v.url for v in get_likes]))
    # print(likes)

    return templating.TemplateResponse("home.html" ,{"request" :request, "url" :urls, "subscribed": count, "likes": likes})


@home.get("/watch_vid/" ,response_class=HTMLResponse)
async def watch(request:Request,db:db_dependency, url:str):
    get_title = db.query(Video).filter_by(url=url).all()

    get_likes = db.query(Likes).filter_by(url=url).all()
    get_comm = db.query(Comments).filter_by(url=url).all()

    likes = list(set([v.user for v in get_likes]))
    comments = list(set([v.comment for v in get_comm]))
    title = list(set([v.title for v in get_title]))
    print(comments)
        # print(likes)
    return templating.TemplateResponse("/watch.html", {"request": request, "url": url , "likes" :likes,"comments" :comments, "title" :title })
