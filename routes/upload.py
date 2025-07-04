from fastapi import APIRouter, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from routes.login import db_dependency
import cloudinary.uploader
from models.models import Video
from pydantic import BaseModel
import db.cloudinary
from routes.login import SECRET_KEYS,ALGORITHM
from jose import jwt

upload = APIRouter()
templating = Jinja2Templates(directory="templates")

class VIDEOBASE(BaseModel):
    url: str
    user :str
    title :str

    class Config :
        orm=True

@upload.get("/upload",response_class=HTMLResponse)
async def uploads(request:Request):
    return templating.TemplateResponse("upload.html",{"request":request})

@upload.post("/upload_video",response_class=HTMLResponse)
async def get_upload(request:Request , db:db_dependency ,file:UploadFile= File(...), title:str=Form(...)): 
    token = request.cookies.get("access_token")
    print(token)
    decoded_token = jwt.decode(token, SECRET_KEYS, algorithms=ALGORITHM)    
    get_user = decoded_token["user"]

    try : 
        result = cloudinary.uploader.upload(
            file.file,
            resource_type= "video"
        )
        url = result.get("secure_url")
        if result : 
            print('done')
            post_video = VIDEOBASE(url=url, user=get_user, title=title)
            post_db = Video(url=post_video.url, user=post_video.user , title=post_video.title)
            db.add(post_db)
            db.commit()
            print("done")
            return RedirectResponse("/" ,status_code=303)


    except Exception as e:
        print(str(e))
