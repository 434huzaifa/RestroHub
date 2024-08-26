from ninja import ModelSchema,Schema
from .models import Restaurant

class RestaurantSchema(ModelSchema):
    class Meta:
        model=Restaurant
        fields = "__all__"

class RestaurantCreateSchema(Schema):
    opening_hours:str="11:30"
    owner_id:int|str=1
    name:str="Sultan Dine"
    address:str="Jatrabari,Dhaka"
    phone_number:str="12345678901"
    description:str="Great restaurant with great test"

class MessageSchema(Schema):
    message:str|None

class LoginResponseSchema(Schema):
    token:str
    expire:str