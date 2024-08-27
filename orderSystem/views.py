from django.http import HttpRequest
from icecream import ic
from ninja import PatchDict
from ninja_extra import api_controller, route
from ninja_extra.permissions import AllowAny

from api.permission import OwnerOnly
from api.schema import MessageSchema
from api.utils import AuthCookie, code400and500
from orderSystem.schema import *
from orderSystem.models import *
from menuSystem.models import Item, Restaurant


# Create your views here.
@api_controller("/order", tags=["Order"], auth=AuthCookie(False))
class OrderAPI:
    @route.post("", response={201: OrderSchema, code400and500: MessageSchema})
    def create_order(self, request, body: OrderCreateSchema):
        data = body.model_dump()
        restaurant = Restaurant.objects.get(id=data.get("restaurant_id"))
        isOwnerOrEmployee = False
        if request.user._meta.object_name == "Owner":
            isOwnerOrEmployee = restaurant.owners.filter(id=request.user.id).exists()
        else:
            isOwnerOrEmployee = restaurant.employees.filter(id=request.user.id).exists()
        if isOwnerOrEmployee:
            orderRows = []
            t_totalPrice = 0.0
            for i in data.get("items"):
                ic(i)
                item = Item.objects.get(id=i.get("item_id"))
                if item.menus.filter(id=data.get("menu_id")).exists():
                    orderRow = OrderRow(item=item, quantity=i.get("quantity"))
                    orderRow.save()
                    t_totalPrice += i.get("quantity") * item.price
                    orderRows.append(orderRow)
                else:
                    return 400,{'message':"Item does not belong to the retaurant"}
                
            order = Order(totalPrice=t_totalPrice, phone=data.get("phone"))
            if data.get("name", None):
                order.name = data.get("name")
            if data.get("description", None):
                order.description = data.get("description")
            order.save()
            order.items.set(orderRows)
            return 201, order
        return 400, {"message": "Owner or Employee mismatch with Retaurant"}
