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
from ninja_extra.permissions import AllowAny

# Create your views here.


@api_controller(
    "/restaurant", tags=["Restaurant"], permissions=[OwnerOnly], auth=AuthCookie(False)
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
            restaurant = Restaurant.objects.create(**data)
            request.user.restaurants.add(restaurant)
            return 201, restaurant
        except Exception as e:
            return 500, {"message": str(e)}

    @route.get(
        "/myrestaurant",
        response={200: list[RestaurantIdNameSchema], code400and500: MessageSchema},
        summary="List all the retaurant of the owner",
    )
    def get_all_my_restaurant(self, request: HttpRequest):
        return 200, request.user.restaurants

    @route.get(
        "",
        response={
            200: RestaurantSchema,
            400: MessageSchema,
            404: MessageSchema,
            500: MessageSchema,
        },
        summary="Get single restaurant information",
        permissions=[AllowAny],
    )
    def get_a_restaurant(self, restaurant_id: int):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        return 200, restaurant

    @route.delete("", response={200: MessageSchema, code400and500: MessageSchema})
    def delete_restaurant(self, request: HttpRequest, restaurant_id: int = None):
        if restaurant_id:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            if restaurant.owners.filter(id=request.user.id).exists():
                message = f'{restaurant.name}"s data deleted'
                return 200, {"message": message}
            return 400, {"message": "You are not owner of this retaurent"}
        return 400, {"message": "Invalid id!"}

    @route.patch(
        "",
        response={201: RestaurantSchema, code400and500: MessageSchema},
        auth=AuthCookie(False),
    )
    def update_restaurant(
        self,
        request: HttpRequest,
        body: PatchDict[RestaurantCreateSchema],
        restaurant_id: int,
    ):
        if restaurant_id:
            restaurant = Restaurant.objects.get(
                id=restaurant_id,
            )
            if not restaurant.owners.filter(id=request.user.id).exists():
                return 400, {"message": "You are not owner of this restaurant"}
            for key, value in body:
                setattr(restaurant, key, value)
            restaurant.save()
            return 201, restaurant
        return 400, {"message": "Invalid id!"}
