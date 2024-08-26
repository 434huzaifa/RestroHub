from ninja_extra import api_controller, route
from .schema import *
from icecream import ic
from .models import *
from userSystem.models import *
from api.schema import MessageSchema
from api.utils import AuthCookie
from django.utils.timezone import datetime

# Create your views here.


@api_controller("/restaurant", tags=["Restaurant"], permissions=[],auth=AuthCookie())
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
    
    

