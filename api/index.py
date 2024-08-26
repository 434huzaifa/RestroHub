from ninja_extra import NinjaExtraAPI
from ninja.security import HttpBearer
from icecream import ic
import jwt
from django.contrib.auth import authenticate
from django.utils.timezone import datetime,timedelta
from os import getenv
from dotenv import load_dotenv
load_dotenv()


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token:
            try:
                return ic(jwt.decode(token,getenv("PROJECT_SECRECT"),algorithms="HS256"))
            except jwt.ExpiredSignatureError:
                ic("Expired")

app = NinjaExtraAPI(
    title="RestroHub APIs",
    description="A simple restaurant managing site. [Admin Panel](http://127.0.0.1:8000/admin)",
    docs_url="/",
)

@app.post("/headerkey",tags=['Authorization'],description="For testing purpose. Enter username and password to get the Bearer token then paste the token into authorization. [see this video to use token](https://www.youtube.com/watch?v=8wxprVcHB5w) \n\nusername: ` Enid21 `\n\npassword:` q `")
def headerKey(request,username=None,password=None):

    if username and password:
        user=authenticate(request, username=username, password=password)
        if user !=None:
      
            timeExp=int((datetime.now()+timedelta(minutes=10)).timestamp())
            return {"token":jwt.encode({'exp':timeExp,'username':user.get_username()},key=getenv("PROJECT_SECRECT")),"expired":(datetime.now()+timedelta(minutes=10)).strftime('%d/%m/%Y, %I:%M:%S %p')}
    return 400,{"message":"username and password failed"}