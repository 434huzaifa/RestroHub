from ninja.security import HttpBearer,APIKeyCookie
from django.http import HttpRequest
from icecream import ic
import jwt
from os import getenv
from dotenv import load_dotenv
load_dotenv()

code400and500=frozenset({400,500})

class AuthBearer(APIKeyCookie):
    def authenticate(self, request:HttpRequest,key):
        if key:
            try:
                return jwt.decode(key,getenv("PROJECT_SECRECT"),algorithms="HS256")
            except jwt.ExpiredSignatureError:
                ic("Expired")