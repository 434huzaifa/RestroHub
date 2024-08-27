from ninja_extra import NinjaExtraAPI
from django.http import HttpRequest, HttpResponse
import jwt
from django.contrib.auth import authenticate
from django.utils.timezone import datetime, timedelta
from restaurantSystem.views import RestaurantAPI
from userSystem.views import UserAPI, EmployeeAPI
from menuSystem.views import MenuApi
from api.utils import code400and500
from os import getenv
from api.schema import *
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from jwt import ExpiredSignatureError,InvalidTokenError

load_dotenv()

app = NinjaExtraAPI(
    title="RestroHub APIs",
    description="A simple restaurant managing site. [Admin Panel](http://127.0.0.1:8000/admin)",
    docs_url="/",
)


@app.post(
    "/headerkey",
    tags=["Authorization"],
    description="For testing purpose. Enter username and password it will automatically set key in cookies. \n\nusername: ` Enid21 `\n\npassword:` q `",
    summary="Use this API first to use locked API.",
    response={200: LoginResponseSchema, code400and500: MessageSchema},
)
def headerKey(
    request: HttpRequest, response: HttpResponse, username=None, password=None
):
    try:
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user != None:
                timeExp = int((datetime.now() + timedelta(minutes=10)).timestamp())
                token = jwt.encode(
                    {"exp": timeExp, "username": user.get_username()},
                    key=getenv("PROJECT_SECRECT"),
                )
                response.set_cookie(
                    "key", token, expires=datetime.now() + timedelta(minutes=10)
                )
                return 200, {
                    "token": token,
                    "expired": (datetime.now() + timedelta(minutes=10)).strftime(
                        "%d/%m/%Y, %I:%M:%S %p"
                    ),
                }
        return 400, {"message": "username and password failed"}
    except Exception as e:
        return 500, str(e)

@app.exception_handler(ObjectDoesNotExist)
def ObjectNotFound(request,exce):
    return app.create_response(request,{"message":f"ObjectDoesNotExist:{exce}"},status=400)

@app.exception_handler(Exception)
def GlobalException(request,exce):
    return app.create_response(request,{"message":f"Exception:{exce}"},status=500)

@app.exception_handler(ExpiredSignatureError)
def JwtExpire(request,exce):
    return app.create_response(request,{"message":f"Expired:{exce}.excute /headerkey api again"},status=400)

@app.exception_handler(InvalidTokenError)
def JwtInvalidToken(request,exce):
    return app.create_response(request,{"message":f"Invalid Token:{exce}.excute /headerkey api again"},status=400)

app.register_controllers(RestaurantAPI)
app.register_controllers(UserAPI)
app.register_controllers(EmployeeAPI)
app.register_controllers(MenuApi)
