
from ninja_extra import api_controller, route
from .schema import *
from django.contrib.auth.models import User
from api.schema import MessageSchema
from icecream import ic
from userSystem.models import *
from api.utils import AuthBearer
from django.http import HttpRequest
from api.permission import OwnerOnly
@api_controller("/owner",tags=['User'])
class UserAPI:
    @route.post("",response={201:OwnerSchemaWithoutRestaurants,400:MessageSchema,500:MessageSchema})
    def create_owner(self,body:UserBodySchema):
        try:
            UserData=body.model_dump(include=('password','username'))
            user=User.objects.create_user(username=UserData['username'],password=UserData['password'])
            if user:
                profileData=body.model_dump(exclude=('password','username'))
                profile=Profile(user=user,phone=profileData['phone'],address=profileData.get('address',None),name=profileData['name'])
                profile.save()
                if profile:
                    owner=Owner(profile=profile)
                    owner.save()
                    return 201,owner
                return 400,{'message':"Profile creation failed!"}
            return 400,{'message':'User creation failed!'}
        except Exception as e:
            return 500,str(e)
    @route.get("",response={200:OwnerSchema,400:MessageSchema,500:MessageSchema},auth=AuthBearer(),permissions=[OwnerOnly])
    def get_owner_information(self,request:HttpRequest):
        try:
            ic(request.auth)
            owner=Owner.objects.filter(profile__user__username=request.auth['username'])
            if len(owner)!=0:
                return 200,owner[0]
            return 400, {"message":"Owner not found!"}
        except Exception as e:
            return 500, str(e)

@api_controller("/employee",tags=['User'])
class EmployeeAPI:
    @route.post("",response={201:EmployeeSchemaWithoutRestaurants,400:MessageSchema,500:MessageSchema})
    def create_employee(self,body:UserBodySchema):
        try:
            UserData=body.model_dump(include=('password','username'))
            user=User.objects.create_user(username=UserData['username'],password=UserData['password'])
            if user:
                profileData=body.model_dump(exclude=('password','username'))
                profile=Profile(user=user,phone=profileData['phone'],address=profileData.get('address',None),name=profileData['name'])
                profile.save()
                if profile:
                    emp=Employee(profile=profile)
                    emp.save()
                    return 201,emp
                return 400,{'message':"Profile creation failed!"}
            return 400,{'message':'User creation failed!'}
        except Exception as e:
            return 500,str(e)
        

