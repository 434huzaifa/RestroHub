from django.http import HttpRequest
from icecream import ic
from ninja import PatchDict
from ninja_extra import api_controller, route
from ninja_extra.permissions import AllowAny

from api.permission import OwnerOnly
from api.schema import MessageSchema
from api.utils import AuthCookie, code400and500
from menuSystem.schema import *

# Create your views here.


@api_controller("/menu", tags=["Menu"], auth=AuthCookie(False), permissions=[OwnerOnly])
class MenuApi:
    @route.post("", response={201: MenuSchema, code400and500: MessageSchema})
    def create_menu(self, request: HttpRequest, body: MenuCreateSchema):
        data = body.model_dump()
        restaurant = Restaurant.objects.get(
            id=data.get("restaurant_id")
        )
        
        if not restaurant.owners.filter(id=request.user.id).exists():
            return 400,{"message":"You are not owner of this restaurant"}
        menu = Menu(restaurant=restaurant, name=data.get("name"))
        menu.save()
        for i in data.get("items"):
            item = Item(name=i.get("name"), price=i.get("price"))
            if i.get("description",None):
                item.description=i.get("description")
            item.save()
            menu.items.add(item)
        return 201, menu

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
        menu = Menu.objects.get(
            id=menu_id, restaurant__id=restaurant_id
        )
        if not menu.restaurant.owners.filter(id=request.user.id).exists():
            return 400,{"message":"You are not owner of this restaurant"}
            
        menu.name = body.get("name")
        return 201, menu
    
    @route.delete(
        "",
        response={200: MessageSchema, code400and500: MessageSchema},
        summary="Delete a menu of a restaurant",
    )
    def change_menu_name(
        self,
        request,
        menu_id: int,
    ):
        menu = Menu.objects.get(
            id=menu_id
        )
        message=f'{menu.name} has been deleted!'
        if not menu.restaurant.owners.filter(id=request.user.id).exists():
            return 400,{"message":"You are not owner of this restaurant"}
        menu.delete()
        return 200, {"message":message}

    @route.get(
        "",
        response={200: MenuWithoutRestaurantSchema, code400and500: MessageSchema},
        summary="Get Single Menu",
        auth=None,
        permissions=[AllowAny]
    )
    def get_single_menu(self, menu_id: int, restaurant_id: int):
        menu = Menu.objects.get(
            id=menu_id, restaurant__id=restaurant_id
        )
        if menu:
            return 200, menu

    @route.get(
        "/all",
        response={200: list[MenuWithoutRestaurantItemsSchema], code400and500: MessageSchema},
        summary="Get All the menu of the restaurant",
        auth=None,
        permissions=[AllowAny]
    )
    def get_all_the_menu(self, restaurant_id: int):
        if restaurant_id:
            return 200, Menu.objects.filter(
                restaurant__id=restaurant_id
            )
        return 400, {"message": "Invalid Id"}
    

    @route.delete(
        "/item",
        response={200: MessageSchema, code400and500: MessageSchema},
        summary="Delete single item from menu of a restaurant",
    )
    def delete_item(self, request, menu_id: int, item_id: int):
        item = Item.objects.get(
            id=item_id,
        )
        if not item.menus.get(id=menu_id).restaurant.owners.filter(id=request.user.id).exists():
            return 400,{"message":"You are not owner of this retaurant"}
        item.delete()
        message = f"{item.name} deleted from menu!"
        return 200, {"message": message}

    @route.post(
        "/item",
        response={201: list[ItemSchema], code400and500: MessageSchema},
        summary="Add single item to a menu",
    )
    def add_item(self, request, body: ItemCreateSchema):
        data = body.model_dump()
        menu = Menu.objects.get(id=data.get("menu_id"))
        
        if not menu.restaurant.owners.filter(id=request.user.id).exists():
            return 400,{"message":"You are not owner of this restaurant"}
        
        item = Item(name=data.get("name"), price=data.get("price"))
        if data.get("description",None):
            item.description=data.get("description",None)
        item.save()
        menu.items.add(item)
        menu.save()
        return 201, menu.items

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
            item = Item.objects.get(
                id=item_id,
                menus__id=menu_id,
                menus__restaurant__id=restaurant_id,
            )
            if not item.menus.get(id=menu_id).restaurant.owners.filter(id=request.user.id).exists():
                return 400,{"message":"You are not an owner of this restaurant"}
            
            if body.get("name", None):
                item.name = body.get("name")
            if body.get("price", None):
                item.price = body.get("price")
            if body.get("description",None):
                item.description = body.get("description")
            item.save()
            return 201, item
        return 400, {"message": "Invalid ID"}
