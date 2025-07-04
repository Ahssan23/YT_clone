from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from routes.login import db_dependency
from jose import jwt
from routes.login import SECRET_KEYS, ALGORITHM
from models.models import Video



subss  = APIRouter()
templating = Jinja2Templates(directory="templates")


@subss.get("/subscribed" ,response_class=HTMLResponse)
async def Subs(request:Request, db:db_dependency):
    token = request.cookies.get("access_token")
    decoded = jwt.decode(token, SECRET_KEYS, algorithms=[ALGORITHM])
    user  = decoded['user']

    get_subs = db.query(Video).filter_by(user=user)
    subs = list([(v.url, v.user, v.title)for v in get_subs])

    return templating.TemplateResponse("/subscriber_feed.html", {"request": request, "subs": subs})
