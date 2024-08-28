from ninja_extra import api_controller, route
from ninja import PatchDict
from .schema import *
from django.contrib.auth.models import User
from api.schema import MessageSchema
from icecream import ic
from userSystem.models import *
from api.utils import AuthCookie
from django.http import HttpRequest
from ninja_extra.permissions import AllowAny
from api.permission import OwnerOnly
from api.utils import code400and500


def createProfie(body) -> list:
    UserData = body.model_dump(include=("password", "username"))
    user = User.objects.create_user(
        username=UserData["username"], password=UserData["password"]
    )

    if user:
        profileData = body.model_dump(exclude=("password", "username"))
        profile = Profile(
            user=user,
            phone=profileData["phone"],
            address=profileData.get("address", None),
            name=profileData["name"],
        )
        profile.save()
        if profile:
            ic()
            return [201, profile]
        return [400, "Profile creation failed!"]
    return [400, "User creation failed!"]


@api_controller("/owner", tags=["Owner"], auth=AuthCookie(), permissions=[OwnerOnly])
class UserAPI:
    @route.post(
        "",
        response={
            201: OwnerSchemaWithoutRestaurants,
            400: MessageSchema,
            500: MessageSchema,
        },
        auth=None,
        permissions=[AllowAny],
    )
    def create_owner(self, body: UserBodySchema):
        try:
            returnData = createProfie(body)
            if returnData[0] == 201:
                owner = Owner(profile=returnData[1])
                owner.save()
                return 201, owner
            else:
                return returnData[0], {"message": returnData[1]}
        except Exception as e:
            return 500, str(e)

    @route.get(
        "",
        response={
            200: OwnerSchemaWithoutRestaurants,
            400: MessageSchema,
            500: MessageSchema,
        },
    )
    def get_owner_information(self, request: HttpRequest):
        return 200, request.user

    @route.patch(
        "",
        response={201: OwnerSchemaWithoutRestaurants, code400and500: MessageSchema},
    )
    def update_owner(self, request: HttpRequest, body: PatchDict[UserPatchBodySchema]):
        owner = request.user
        if body.get("username", None):
            owner.profile.user.username = body.save()
            owner.profile.user.save()
        body.pop("username")
        for key, value in body:
            setattr(owner, key, value)
        owner.profile.save()
        return 201, owner

    @route.delete(
        "",
        response={200: MessageSchema, code400and500: MessageSchema},
    )
    def delete_owner_data(self, request: HttpRequest):
        message = f'{request.user.profile.user.username}"s all data has been deleted!'
        request.user.delete()
        return 200, {"message": message}


@api_controller("/employee", tags=["Employee"], auth=AuthCookie())
class EmployeeAPI:
    @route.post(
        "",
        response={
            201: EmployeeSchemaWithoutRestaurants,
            400: MessageSchema,
            500: MessageSchema,
        },
        auth=None,
    )
    def create_employee(self, body: UserBodySchema):
        try:
            returnData = createProfie(body)
            if returnData[0] == 201:
                emp = Employee(profile=returnData[1])
                emp.save()
                return 201, emp
            else:
                return returnData[0], {"message": returnData[1]}
        except Exception as e:
            return 500, str(e)

    @route.get(
        "",
        response={200: EmployeeSchema, 400: MessageSchema, 500: MessageSchema},
    )
    def get_employee_information(self, request: HttpRequest):
        return 200, request.user

    @route.delete(
        "",
        response={200: MessageSchema, code400and500: MessageSchema},
    )
    def delete_employee_data(self, request: HttpRequest):
        message = f'{request.user.profile.user.username}"s all data has been deleted!'
        request.user.delete()
        return 200, {"message": message}

    @route.patch(
        "",
        response={201: EmployeeSchemaWithoutRestaurants, code400and500: MessageSchema},
    )
    def update_employee(
        self, request: HttpRequest, body: PatchDict[UserPatchBodySchema]
    ):
        emp = request.user
        if body.get("username", None):
            emp.profile.user.username = body.save()
            emp.profile.user.save()
        body.pop("username")
        for key, value in body:
            setattr(emp, key, value)
        emp.profile.save()
        return 201, emp
