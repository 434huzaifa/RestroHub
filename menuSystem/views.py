from api.permission import OwnerOnly
from django.http import HttpRequest
from api.utils import code400and500
from api.schema import MessageSchema
from api.utils import AuthCookie
from icecream import ic
from ninja_extra import api_controller, route
from ninja import PatchDict
from menuSystem.schema import *
# Create your views here.

@api_controller("/menu",tags=["Menu"],auth=AuthCookie(False),permissions=[OwnerOnly])
class MenuApi:
    @route.post("",response={201:MenuWithoutItemSchema,code400and500:MessageSchema})
    def create_menu(self,request:HttpRequest,body:MenuCreateSchema):
        ic(request.user)
        data=body.model_dump()
        restaurant=Restaurant.objects.get(id=data.get('restaurant_id'),owners=request.user)
        if restaurant:
            return 400,{"message":"ahuza2"}
        return 400,{"message":"ahuza"}
        