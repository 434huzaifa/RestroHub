from ninja_extra import NinjaExtraAPI, api_controller, route
from .schema import *
from icecream import ic
from .models import *
from userSystem.models import *
from ninja.security import HttpBearer
import jwt
from django.contrib.auth import authenticate
from django.utils.timezone import datetime,timedelta

from os import getenv
from dotenv import load_dotenv
load_dotenv()
# Create your views here.

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

@app.post("/headerkey",tags=['Authorization'],description="For testing purpose. \nusername: ` Enid21 `\npassword:` q `")
def headerKey(request,username=None,password=None):

    if username and password:
        user=authenticate(request, username=username, password=password)
        if user !=None:
            ic(user.get_username())
            timeExp=int((datetime.now()+timedelta(minutes=10)).timestamp())
            return {"token":jwt.encode({'exp':timeExp,'username':user.get_username()},key=getenv("PROJECT_SECRECT")),"expired":(datetime.now()+timedelta(minutes=10)).strftime('%d/%m/%Y, %I:%M:%S %p')}
    return 400,{"message":"username and password failed"}


@api_controller("/restaurant", tags=["Restaurant"], permissions=[],auth=AuthBearer())
class RestaurantAPI:
    @route.post(
        "",
        response={201: RestaurantSchema, 400: MessageSchema, 500: MessageSchema},
        summary="Create Restaurant data",
    )
    def create(self,body: RestaurantCreateSchema):
        try:
            
            data = body.model_dump()
            data["opening_hours"] = datetime.strptime(
                data["opening_hours"], "%H:%M"
            ).time()
            owner=Owner.objects.filter(id=data.pop('owner_id'))
            if len(owner)!=0:
                restaurant = Restaurant.objects.create(**data)
                owner[0].restaurants.add(restaurant)
                return 201, restaurant
            return 400,{"message":"Owner not found!"}
        except Exception as e:
            return 500, {"message": str(e)}
    @route.get("",response={200:list[RestaurantSchema],400: MessageSchema, 404: MessageSchema,500: MessageSchema})
    def get(self,request,owner_id=None):
        ic(request.auth)
        if owner_id:
            owner=Owner.objects.filter(id=owner_id)
            if len(owner)!=0:
                return 200,owner[0].restaurants
            return 400,{"message":"Owner not found!"}
    
    
app.register_controllers(RestaurantAPI)
