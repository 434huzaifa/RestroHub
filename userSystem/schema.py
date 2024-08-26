from ninja import ModelSchema
from .models import Profiles

class ProfilesSchema(ModelSchema):
    class Meta:
        model=Profiles
        fields = "__all__"