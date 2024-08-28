from ninja import ModelSchema, Schema
from .models import Restaurant
from menuSystem.schema import MenuIdNameSchema

class RestaurantSchema(ModelSchema):
    menus:list[MenuIdNameSchema]
    class Meta:
        model = Restaurant
        fields = "__all__"

class RestaurantIdNameSchema(ModelSchema):
    class Meta:
        model=Restaurant
        fields=['id','name']

class RestaurantCreateSchema(Schema):
    opening_hours: str = "11:30"
    name: str = "Sultan Dine"
    address: str = "Jatrabari,Dhaka"
    phone_number: str = "12345678901"
    description: str = "Great restaurant with great test"

