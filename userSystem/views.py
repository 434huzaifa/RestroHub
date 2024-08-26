
from ninja_extra import api_controller, route
from .schema import *
from django.contrib.auth.models import User
from api.schema import MessageSchema
from icecream import ic
from userSystem.models import *
@api_controller("/user",tags=['User'])
class UserAPI:
    @route.post("/owner",response={201:OwnerSchemaWithoutRestaurants,400:MessageSchema,500:MessageSchema})
    def create_owner(self,body:UserBodySchema):
        try:
            UserData=body.model_dump(include=('password','username'))
            user=User.objects.create(**UserData)
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
    
    @route.post("/employee",response={201:EmployeeSchemaWithoutRestaurants,400:MessageSchema,500:MessageSchema})
    def create_employee(self,body:UserBodySchema):
        try:
            UserData=body.model_dump(include=('password','username'))
            user=User.objects.create(**UserData)
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
        

