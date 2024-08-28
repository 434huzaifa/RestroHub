from django.http import HttpRequest
from ninja_extra import ControllerBase, permissions
from icecream import ic
from restaurantSystem.models import Restaurant

class OwnerOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: ControllerBase) -> bool:
        if request.user._meta.object_name == "Owner":
            return True

def OwnerOrEmployeeCheck(restaurant: Restaurant, request) -> bool:
    isOwnerOrEmployee = False
    if request.user._meta.object_name == "Owner":
        isOwnerOrEmployee = restaurant.owners.filter(id=request.user.id).exists()
    else:
        isOwnerOrEmployee = restaurant.employees.filter(id=request.user.id).exists()
    return isOwnerOrEmployee
