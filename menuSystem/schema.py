from ninja import ModelSchema,Schema,Field
from menuSystem.models import *
from restaurantSystem.schema import RestaurantSchema
class ItemSchema(ModelSchema):
    class Meta:
        model=Item
        fields='__all__'

class MenuSchema(ModelSchema):
    restaurant:RestaurantSchema
    items:list[ItemSchema]
    class Meta:
        model=Menu
        fields='__all__'

class MenuWithoutItemSchema(ModelSchema):
    restaurant:RestaurantSchema
    class Meta:
        model=Menu
        fields='__all__'
        exclude=['items']

class ItemCreateSchema(Schema):
    name:str=Field(max_length=100)
    price:float

class MenuCreateSchema(Schema):
    restaurant_id:int=1
    items:list[ItemCreateSchema]=[{"name":"Briyani","price":150.0}]