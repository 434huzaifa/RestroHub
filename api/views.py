from ninja_extra import NinjaExtraAPI
from django.http import HttpRequest, HttpResponse
import jwt
from django.contrib.auth import authenticate,logout
from django.utils.timezone import datetime, timedelta
from restaurantSystem.views import RestaurantAPI
from userSystem.views import UserAPI, EmployeeAPI
from menuSystem.views import MenuApi
from api.utils import code400and500
from os import getenv
from icecream import ic
from api.schema import *
from dotenv import load_dotenv
from django.core.exceptions import ObjectDoesNotExist
from jwt import ExpiredSignatureError,InvalidTokenError
import sys
import traceback

load_dotenv()

app = NinjaExtraAPI(
    title="RestroHub APIs",
    description="A simple restaurant managing site. [Admin Panel](http://127.0.0.1:8000/admin)",
    docs_url="/",
)


@app.post(
    "/login",
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
                timeExp = int((datetime.now() + timedelta(hours=1)).timestamp())
                token = jwt.encode(
                    {"exp": timeExp, "username": user.get_username()},
                    key=getenv("PROJECT_SECRECT"),
                )
                response.set_cookie(
                    "key", token, expires=datetime.now() + timedelta(minutes=10)
                )
                return 200, {
                    "token": token,
                    "expired": (datetime.now() + timedelta(hours=1)).strftime(
                        "%d/%m/%Y, %I:%M:%S %p"
                    ),
                }
        return 400, {"message": "username and password failed"}
    except Exception as e:
        return 500, str(e)


@app.get("/logout",tags=["Authorization"],
    response={200: MessageSchema, code400and500: MessageSchema},)
def logout(request:HttpRequest,response: HttpResponse,):
    logout(request)
    response.cookies.clear()
    return 200,{"message":"Logout Successfull"}
    

@app.exception_handler(ObjectDoesNotExist)
def ObjectNotFound(request,exce):
    return app.create_response(request,{"message":f"ObjectDoesNotExist:{exce}"},status=404)

@app.exception_handler(Exception)
def GlobalException(request,exce):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    error_message = f"{exc_type.__name__}: {str(exc_value)}"
    error_details = traceback.format_exc()
    
    ic("Error occurred:")
    print(error_message)
    ic("Detailed error trace:")
    print(error_details)
    return app.create_response(request,{"message":f"Exception:{exce}"},status=500)

@app.exception_handler(ExpiredSignatureError)
def JwtExpire(request,exce):
    return app.create_response(request,{"message":f"Expired:{exce}.excute /login api again"},status=400)

@app.exception_handler(InvalidTokenError)
def JwtInvalidToken(request,exce):
    return app.create_response(request,{"message":f"Invalid Token:{exce}.excute /login api again"},status=400)

app.register_controllers(RestaurantAPI)
app.register_controllers(UserAPI)
app.register_controllers(EmployeeAPI)
app.register_controllers(MenuApi)
