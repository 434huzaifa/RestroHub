from ninja import ModelSchema
from .models import Restaurant
from userSystem.schema import ProfilesSchema

class RestaurantSchema(ModelSchema):
    owner:ProfilesSchema
    class Meta:
        model=Restaurant
        fields = "__all__"