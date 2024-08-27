from django.http import HttpRequest
from ninja_extra import ControllerBase, permissions
from userSystem.schema import Owner, Employee
from icecream import ic
class OwnerOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: ControllerBase) -> bool:
        if request.user._meta.object_name == "Owner":
            return True

