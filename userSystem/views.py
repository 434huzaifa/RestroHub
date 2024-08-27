from ninja_extra import api_controller, route
from ninja import PatchDict
from .schema import *
from django.contrib.auth.models import User
from api.schema import MessageSchema
from icecream import ic
from userSystem.models import *
from api.utils import AuthCookie
from django.http import HttpRequest
from api.permission import OwnerOnly
from api.utils import code400and500


def createProfie(model_dump) -> list:
    UserData = model_dump(include=("password", "username"))
    user = User.objects.create_user(
        username=UserData["username"], password=UserData["password"]
    )

    if user:
        profileData = model_dump(exclude=("password", "username"))
        profile = Profile(
            user=user,
            phone=profileData["phone"],
            address=profileData.get("address", None),
            name=profileData["name"],
        )
        profile.save()
        if profile:

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
        permissions=None,
    )
    def create_owner(self, body: UserBodySchema):
        try:
            returnData = createProfie(body.model_dump())
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
        try:
            owner = Owner.objects.filter(
                profile__user__username=request.auth["username"]
            )
            if len(owner) != 0:
                return 200, owner[0]
            return 400, {"message": "Owner not found!"}
        except Exception as e:
            return 500, str(e)

    @route.patch(
        "",
        response={201: OwnerSchemaWithoutRestaurants, code400and500: MessageSchema},
    )
    def update_owner(self, request: HttpRequest, body: PatchDict[UserPatchBodySchema]):
        owner = Owner.objects.filter(profile__user__username=request.auth["username"])
        if len(owner) != 0:
            owner = owner[0]
            if body.get("username", None):
                owner.profile.user.username = body.save()
                owner.profile.user.save()
            if body.get("phone", None):
                owner.profile.phone = body["phone"]
            if body.get("address", None):
                owner.profile.address = body["address"]
            if body.get("name", None):
                owner.profile.name = body["name"]
            owner.profile.save()
            return 201, owner
        return 400, {"message": "Owner not found!"}

    @route.delete(
        "",
        response={200: MessageSchema, code400and500: MessageSchema},
    )
    def delete_owner_data(self, request: HttpRequest):
        owners = Owner.objects.filter(profile__user__username=request.auth["username"])
        if len(owners) != 0:
            message = f'{owners[0].profile.user.username}"s all data has been deleted!'
            owners[0].delete()
            return 200, {"message": message}
        return 400, {"message": "Owner not found!"}


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
            returnData = createProfie(body.model_dump())
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
        try:
            employee = Employee.objects.filter(
                profile__user__username=request.auth["username"]
            )
            if len(employee) != 0:
                return 200, employee[0]
            return 400, {"message": "Employee not found!"}
        except Exception as e:
            return 500, str(e)

    @route.delete(
        "",
        response={200: MessageSchema, code400and500: MessageSchema},
    )
    def delete_employee_data(self, request: HttpRequest):
        emps = Employee.objects.filter(profile__user__username=request.auth["username"])
        if len(emps) != 0:
            message = f'{emps[0].profile.user.username}"s all data has been deleted!'
            emps[0].delete()
            return 200, {"message": message}
        return 400, {"message": "Employee not found!"}

    @route.patch(
        "",
        response={201: EmployeeSchemaWithoutRestaurants, code400and500: MessageSchema},
    )
    def update_employee(
        self, request: HttpRequest, body: PatchDict[UserPatchBodySchema]
    ):
        emp = Employee.objects.filter(profile__user__username=request.auth["username"])
        if len(emp) != 0:
            emp = emp[0]
            if body.get("username", None):
                emp.profile.user.username = body.save()
                emp.profile.user.save()
            if body.get("phone", None):
                emp.profile.phone = body["phone"]
            if body.get("address", None):
                emp.profile.address = body["address"]
            if body.get("name", None):
                emp.profile.name = body["name"]
            emp.profile.save()
            return 201, emp
        return 400, {"message": "Employee not found!"}
