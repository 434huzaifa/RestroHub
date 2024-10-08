from ninja import ModelSchema, Schema, Field
from menuSystem.models import *


class ItemSchema(ModelSchema):
    class Meta:
        model = Item
        fields = "__all__"


class ItemPatchSchema(ModelSchema):
    class Meta:
        model = Item
        fields = "__all__"
        exclude = ["id"]


class MenuSchema(ModelSchema):
    items: list[ItemSchema]

    class Meta:
        model = Menu
        fields = "__all__"


class MenuIdNameSchema(ModelSchema):
    class Meta:
        model = Menu
        fields = ["id", "name"]


class MenuWithoutItemsSchema(ModelSchema):
    class Meta:
        model = Menu
        fields = "__all__"
        exclude = ["items"]


class MenuChangeNameSchema(Schema):
    name: str = Field(max_length=100, default="Chessy Menu")


class MenuWithoutItemSchema(ModelSchema):
    class Meta:
        model = Menu
        fields = "__all__"
        exclude = ["items"]


class ItemCreateSchema(Schema):
    menu_id: int = 1
    restaurant_id: int = 1
    description: str | None = None
    name: str = Field(max_length=100, default="Chawmin")
    price: float = 120


class MenuCreateSchema(Schema):
    restaurant_id: int = 1
    name: str | None = "Summer Menu"
    items: list[ItemCreateSchema] = [
        {"name": "Briyani", "price": 150.0, "description": "Potato,Lamb,Chatni"}
    ]
