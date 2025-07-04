from fastapi import FastAPI
from routes.login import login
from routes.home import home
from routes.upload import upload
from routes.subscibe import subs
from routes.profiles import profile_app
from routes.likes import like
from routes.comments import comment
from routes.subsciber_feed import subss

app = FastAPI()
app.include_router(login)
app.include_router(home)
app.include_router(upload)
app.include_router(subs)
app.include_router(profile_app)
app.include_router(like)
app.include_router(comment)
app.include_router(subss)