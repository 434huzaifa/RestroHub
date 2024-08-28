from django.http import HttpRequest
from icecream import ic
from ninja import PatchDict
from ninja_extra import api_controller, route
from ninja_extra.permissions import AllowAny

from api.permission import OwnerOnly
from api.schema import MessageSchema
from api.utils import AuthCookie, code400and500
from menuSystem.schema import *
from restaurantSystem.models import Restaurant

# Create your views here.


@api_controller("/menu", tags=["Menu"], auth=AuthCookie(False), permissions=[OwnerOnly])
class MenuApi:
    @route.post("", response={201: MenuSchema, code400and500: MessageSchema})
    def create_menu(self, request: HttpRequest, body: MenuCreateSchema):
        data = body.model_dump()
        restaurant = Restaurant.objects.get(id=data.get("restaurant_id"))
        if restaurant.owners.filter(id=request.user.id).exists():
            menu = Menu(name=data.get("name"))
            menu.save()
            t_items = []
            for i in data.get("items"):
                item = Item(name=i.get("name"), price=i.get("price"))
                if i.get("description", None):
                    item.description = i.get("description")
                item.save()
                t_items.append(item)
            menu.items.set(t_items)
            menu.save()
            restaurant.menus.add(menu)
            return 201, menu
        return 400, {"message": "You are not owner of this restaurant"}

    @route.patch(
        "",
        response={201: MenuWithoutItemSchema, code400and500: MessageSchema},
        summary="Change the name of the menu",
    )
    def change_menu_name(
        self,
        request,
        body: PatchDict[MenuChangeNameSchema],
        restaurant_id: int,
        menu_id: int,
    ):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        if restaurant.owners.filter(id=request.user.id).exists():
            menu = restaurant.menus.get(id=menu_id)
            menu.name = body.get("name")
            return 201, menu
        return 400, {"message": "You are not owner of this restaurant"}

    @route.delete(
        "",
        response={200: MessageSchema, code400and500: MessageSchema},
        summary="Delete a menu of a restaurant",
    )
    def delete_menu(
        self,
        request,
        menu_id: int,
        restaurant_id: int,
    ):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        if restaurant.owners.filter(id=request.user.id).exists():
            menu = restaurant.menus.get(id=menu_id)
            message = f"{menu.name} has been deleted!"
            for i in menu.items.filter():
                i.delete()
            menu.delete()
            return 200, {"message": message}
        return 400, {"message": "You are not owner of this restaurant"}

    @route.get(
        "",
        response={200: MenuSchema, code400and500: MessageSchema},
        summary="Get Single Menu",
        auth=None,
        permissions=[AllowAny],
    )
    def get_single_menu(self, menu_id: int, restaurant_id: int):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        menu = menu = restaurant.menus.get(id=menu_id)
        return 200, menu

    @route.get(
        "/all",
        response={200: list[MenuWithoutItemSchema], code400and500: MessageSchema},
        summary="Get All the menu of the restaurant",
        auth=None,
        permissions=[AllowAny],
    )
    def get_all_the_menu(self, restaurant_id: int):
        if restaurant_id:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            return 200, restaurant.menus
        return 400, {"message": "Invalid Id"}

    @route.delete(
        "/item",
        response={200: MessageSchema, code400and500: MessageSchema},
        summary="Delete single item from menu of a restaurant",
    )
    def delete_item(self, request, menu_id: int, item_id: int, restaurant_id: int):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        menu = restaurant.menus.get(id=menu_id)
        item = menu.items.get(id=item_id)
        if restaurant.owners.filter(id=request.user.id).exists():
            item.delete()
            message = f"{item.name} deleted from menu!"
            if menu.items.count() == 0:
                menu.delete()
            return 200, {"message": message}
        return 400, {"message": "You are not owner of this retaurant"}

    @route.post(
        "/item",
        response={201: list[ItemSchema], code400and500: MessageSchema},
        summary="Add single item to a menu",
    )
    def add_item(self, request, body: ItemCreateSchema):
        data = body.model_dump()
        restaurant = Restaurant.objects.get(id=data.get("restaurant_id"))
        menu = restaurant.menus.get(id=data.get("menu_id"))
        if restaurant.owners.filter(id=request.user.id).exists():
            item = Item(name=data.get("name"), price=data.get("price"))
            if data.get("description", None):
                item.description = data.get("description", None)
            item.save()
            menu.items.add(item)
            menu.save()
            return 201, menu.items
        return 400, {"message": "You are not owner of this restaurant"}

    @route.patch(
        "/item",
        response={201: ItemSchema, code400and500: MessageSchema},
        summary="Update Item informations",
    )
    def update_item(
        self,
        request,
        body: PatchDict[ItemPatchSchema],
        restaurant_id: int,
        menu_id: int,
        item_id: int,
    ):
        if item_id:
            restaurant = Restaurant.objects.get(id=restaurant_id)
            if restaurant.owners.filter(id=request.user.id).exists():
                menu = restaurant.menus.get(id=menu_id)
                item = menu.items.get(id=item_id)
                for key, value in body:
                    setattr(item, key, value)
                item.save()
                return 201, item
            return 400, {"message": "You are not an owner of this restaurant"}
        return 400, {"message": "Invalid ID"}
