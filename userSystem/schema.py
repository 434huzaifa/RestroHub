from ninja import ModelSchema, Schema, Field

from .models import *
from restaurantSystem.schema import RestaurantSchema
from django.contrib.auth.models import User
from icecream import ic


class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ["username"]


class ProfilesSchema(ModelSchema):
    user: UserSchema

    class Meta:
        model = Profile
        fields = "__all__"


class OwnerSchema(ModelSchema):
    profile: ProfilesSchema
    restaurants: list[RestaurantSchema]

    class Meta:
        model = Owner
        fields = "__all__"


class OwnerSchemaWithoutRestaurants(ModelSchema):
    profile: ProfilesSchema

    class Meta:
        model = Owner
        fields = "__all__"
        exclude = ["restaurants"]


class EmployeeSchema(ModelSchema):
    profile: ProfilesSchema
    restaurant: RestaurantSchema = None

    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeSchemaWithoutRestaurants(ModelSchema):
    profile: ProfilesSchema

    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ["restaurant"]


class UserBodySchema(Schema):
    username: str = Field(max_length=50, default="darksoul434")
    password: str = Field(default="q")
    phone: str = Field(default="123456789", max_length=15)
    address: str | None = None
    name: str = Field(default="Hugh Man", max_length=100)


class UserPatchBodySchema(Schema):
    username: str = Field(max_length=50, default="darksoul434")
    phone: str = Field(default="123456789", max_length=15)
    address: str | None = None
    name: str = Field(default="Hugh Man", max_length=100)
