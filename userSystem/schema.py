from ninja import ModelSchema
from .models import *
from restaurantSystem.schema import RestaurantSchema
class ProfilesSchema(ModelSchema):
    class Meta:
        model=Profile
        fields = "__all__"
        
class OwnerSchema(ModelSchema):
    profile:ProfilesSchema
    restaurants:RestaurantSchema
    class Meta:
        model= Owner
        fields = "__all__"

class EmployeeSchema(ModelSchema):
    profile:ProfilesSchema
    restaurants:RestaurantSchema
    class Meta:
        model=Employee
        fields = "__all__"
        