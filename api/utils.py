from ninja.security import HttpBearer
from icecream import ic
import jwt
from os import getenv
from dotenv import load_dotenv
load_dotenv()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token:
            try:
                return ic(jwt.decode(token,getenv("PROJECT_SECRECT"),algorithms="HS256"))
            except jwt.ExpiredSignatureError:
                ic("Expired")