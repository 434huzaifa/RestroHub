from ninja.security import HttpBearer, APIKeyCookie
from django.http import HttpRequest
from icecream import ic
import jwt
from os import getenv
from dotenv import load_dotenv
from userSystem.models import Owner,Employee

load_dotenv()

code400and500 = frozenset({400, 500})


class AuthCookie(APIKeyCookie):
    def authenticate(self, request: HttpRequest, key):
        if key:
            decoded = jwt.decode(key, getenv("PROJECT_SECRECT"), algorithms="HS256")
            ic(decoded)
            owner = Owner.objects.filter(
                profile__user__username=decoded.get("username",None)
            )
            if len(owner) != 0:
                request.user=owner[0]
            emp = Employee.objects.filter(
                profile__user__username=decoded.get("username",None)
            )
            if len(emp) != 0:
                request.user = emp[0]
            if request.user._meta.object_name not in ["Owner","Employee"]:
                raise Exception("User is not and Owner or Employee. User is Alien.")
            ic(request.user._meta.object_name)
            ic(request.user.id)
            return decoded

