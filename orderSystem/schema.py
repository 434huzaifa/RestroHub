from ninja import ModelSchema, Schema, Field
from orderSystem.models import *
from menuSystem.schema import ItemSchema
from restaurantSystem.schema import RestaurantIdNameSchema
class OrderRowSchema(ModelSchema):
    item:ItemSchema
    class Meta:
        model=OrderRow
        fields='__all__'

class OrderSchema(ModelSchema):
    items:list[OrderRowSchema]
    restaurant:RestaurantIdNameSchema
    class Meta:
        model=Order
        fields='__all__'
        
class OrderRowCreateSchema(Schema):
    item_id:int=Field(gt=0,examples=[1])
    quantity:int=Field(gt=0,examples=[2])


class OrderCreateSchema(Schema):
    restaurant_id:int=Field(examples=[1])
    menu_id:int=Field(examples=[1])
    items:list[OrderRowCreateSchema]
    name:str=Field(max_length=100,examples=["Huzaifa"])
    phone:str=Field(max_length=100,examples=["112312312"])
    description:str|None="This is a description....."
    
class SingleOrderCreateSchema(Schema):
    order_id:int=Field(examples=[1])
    restaurant_id:int=Field(examples=[1])
    menu_id:int=Field(examples=[1])
    items:OrderRowCreateSchema
    