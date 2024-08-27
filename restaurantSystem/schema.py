from ninja import ModelSchema,Schema
from .models import Restaurant

class RestaurantSchema(ModelSchema):
    class Meta:
        model=Restaurant
        fields = "__all__"

class RestaurantCreateSchema(Schema):
    opening_hours:str="11:30"
    name:str="Sultan Dine"
    address:str="Jatrabari,Dhaka"
    phone_number:str="12345678901"
    description:str="Great restaurant with great test"


