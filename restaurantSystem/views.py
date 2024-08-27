from ninja_extra import api_controller, route
from ninja import PatchDict
from .schema import *
from icecream import ic
from .models import *
from userSystem.models import *
from api.schema import MessageSchema
from api.utils import AuthCookie
from django.utils.timezone import datetime
from api.permission import OwnerOnly
from django.http import HttpRequest
from api.utils import code400and500
# Create your views here.

@api_controller(
    "/restaurant", tags=["Restaurant"], permissions=[OwnerOnly], auth=AuthCookie()
)
class RestaurantAPI:
    @route.post(
        "",
        response={201: RestaurantSchema, 400: MessageSchema, 500: MessageSchema},
        summary="Create Restaurant data",
    )
    def create(self, body: RestaurantCreateSchema, request: HttpRequest):
        try:

            data = body.model_dump()
            data["opening_hours"] = datetime.strptime(
                data["opening_hours"], "%H:%M"
            ).time()
            owner = Owner.objects.filter(
                profile__user__username=request.auth["username"]
            )
            if len(owner) != 0:
                restaurant = Restaurant.objects.create(**data)
                owner[0].restaurants.add(restaurant)
                return 201, restaurant
            return 400, {"message": "Owner not found!"}
        except Exception as e:
            return 500, {"message": str(e)}

    @route.get(
        "",
        response={
            200: RestaurantSchema,
            400: MessageSchema,
            404: MessageSchema,
            500: MessageSchema,
        },
    )
    def get(self, request: HttpRequest, restaurant_id: int):
        restaurant = Restaurant.objects.filter(id=restaurant_id,owners__profile__user__username=request.auth['username'])
        if len(restaurant) != 0:
            return 200, restaurant[0]
        return 400, {"message": "Restaurant not found!"}

    @route.delete("", response={200: MessageSchema, code400and500: MessageSchema})
    def delete_restaurant(self, request: HttpRequest, restaurant_id: int = None):
        if restaurant_id:
            restaurant = Restaurant.objects.filter(id=restaurant_id,owners__profile__user__username=request.auth['username'])
            if len(restaurant) != 0:
                message = f'{restaurant[0].name}"s data deleted'
                restaurant[0].delete()
                return 200, {"message": message}
            return 400, {"message": "Restaurant not found!"}
        return 400, {"message": "Invalid id!"}


    @route.patch("", response={201: RestaurantSchema, code400and500: MessageSchema},auth=AuthCookie(False))
    def update_restaurant(
        self,
        request: HttpRequest,
        body: PatchDict[RestaurantCreateSchema],
        restaurant_id: int,
    ):
        if restaurant_id:
            restaurant = Restaurant.objects.filter(id=restaurant_id,owners__profile__user__username=request.auth['username'])
            if len(restaurant) != 0:
                restaurant = restaurant[0]
                for i in body:
                    setattr(restaurant, i, body[i])
                restaurant.save()
                return 201, restaurant
            return 400, {"message": "Restaurant not found!"}
        return 400, {"message": "Invalid id!"}
