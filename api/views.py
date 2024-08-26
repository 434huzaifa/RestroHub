from ninja_extra import NinjaExtraAPI
from django.http import HttpRequest,HttpResponse
import jwt
from django.contrib.auth import authenticate
from django.utils.timezone import datetime,timedelta
from restaurantSystem.views import RestaurantAPI
from userSystem.views import UserAPI
from os import getenv
from dotenv import load_dotenv
load_dotenv()





app = NinjaExtraAPI(
    title="RestroHub APIs",
    description="A simple restaurant managing site. [Admin Panel](http://127.0.0.1:8000/admin)",
    docs_url="/",
)



@app.post("/headerkey",tags=['Authorization'],description="For testing purpose. Enter username and password to get the Bearer token then paste the token into authorization. [see this video to use token](https://www.youtube.com/watch?v=8wxprVcHB5w) \n\nusername: ` Enid21 `\n\npassword:` q `")
def headerKey(request:HttpRequest,response:HttpResponse,username=None,password=None):

    if username and password:
        user=authenticate(request, username=username, password=password)
        if user !=None:
      
            timeExp=int((datetime.now()+timedelta(minutes=10)).timestamp())
            
            token=jwt.encode({'exp':timeExp,'username':user.get_username()},key=getenv("PROJECT_SECRECT"))
            response.set_cookie('token',token)
            return {"token":token,"expired":(datetime.now()+timedelta(minutes=10)).strftime('%d/%m/%Y, %I:%M:%S %p')}
    return 400,{"message":"username and password failed"}

app.register_controllers(RestaurantAPI)
app.register_controllers(UserAPI)