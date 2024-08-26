
from django.http import HttpRequest
from ninja_extra import ControllerBase, permissions
from userSystem.schema import Owner
class OwnerOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, controller: ControllerBase) -> bool:
        if request.COOKIES.get("key",None):
            owner=Owner.objects.filter(profile__user__username=request.auth['username'])
            if len(owner)!=0:
                request.auth['isOwner']=True
                return request.method in permissions.SAFE_METHODS
        