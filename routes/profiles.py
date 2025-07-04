from fastapi import APIRouter,Request,Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from routes.login import db_dependency
from models.models import Video, Subs
from jose import jwt
from routes.login import SECRET_KEYS, ALGORITHM

profile_app = APIRouter()
templating = Jinja2Templates(directory="templates")




@profile_app.post("/profile", response_class=HTMLResponse)
async def profile_get(request:Request, db:db_dependency, account_name:str=Form(...)):
    get_subs = db.query(Subs).filter_by(subbed=account_name).count()
    get_vids = db.query(Video).filter_by(user=account_name).all()
    urls = list([(v.url) for v in get_vids])
    


    return templating.TemplateResponse("profile.html", {"request" :request, "total_subs": get_subs, "url": urls })