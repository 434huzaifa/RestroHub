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
from menuSystem.models import Item
from restaurantSystem.models import Restaurant


# Create your views here.

def OwnerOrEmployeeCheck(restaurant:Restaurant,request)->bool:
    isOwnerOrEmployee = False
    if request.user._meta.object_name == "Owner":
        isOwnerOrEmployee = restaurant.owners.filter(id=request.user.id).exists()
    else:
        isOwnerOrEmployee = restaurant.employees.filter(id=request.user.id).exists()
    return isOwnerOrEmployee
        
@api_controller("/order", tags=["Order"], auth=AuthCookie(False))
class OrderAPI:
    @route.post("", response={201: OrderSchema, code400and500: MessageSchema},summary="Create order with multiple items at once")
    def create_order(self, request, body: OrderCreateSchema):
        data = body.model_dump()
        restaurant = Restaurant.objects.get(id=data.get("restaurant_id"))
        if OwnerOrEmployeeCheck(restaurant,request):
            menu=restaurant.menus.get(id=data.get("menu_id"))
            orderRows = []
            t_totalPrice = 0.0
            for i in data.get("items"):
                item = menu.items.get(id=i.get("item_id"))
                orderRow = OrderRow(item=item, quantity=i.get("quantity"))
                orderRow.save()
                t_totalPrice += i.get("quantity") * item.price
                orderRows.append(orderRow)
                
            order = Order(totalPrice=t_totalPrice,restaurant=restaurant, phone=data.get("phone"))
            if data.get("name", None):
                order.name = data.get("name")
            if data.get("description", None):
                order.description = data.get("description")
            order.save()
            order.items.set(orderRows)
            return 201, order
        return 400, {"message": "Owner or Employee mismatch with Restaurant"}
    
    @route.post("/single",response={201:OrderSchema,code400and500:MessageSchema},summary="Add single items to existing order ")
    def add_single_order(self,request,body:SingleOrderCreateSchema):
        data=body.model_dump()
        order=Order.objects.get(id=data.get('order_id'))
        if OwnerOrEmployeeCheck(order.restaurant,request):
            menu=order.restaurant.menus.get(id=data.get("menu_id"))
            item = menu.items.get(id=data.get("item_id"))
            orderRow = OrderRow(item=item, quantity=data.get("quantity"))
            orderRow.save()
            order.totalPrice += data.get("quantity") * item.price
            order.items.add(orderRow)
            order.save()
            return 400,{'message':"Item does not belong to the restaurant"}
        return 400, {"message": "Owner or Employee mismatch with Restaurant"}
    
    @route.delete("/item",response={200:MessageSchema,code400and500:MessageSchema},summary="Delete item from a order")
    def delete_item(self,request,order_row_id:int,order_id:int):
        order=Order.objects.get(id=order_id)
        orderRow=OrderRow.objects.get(id=order_row_id)
        order.totalPrice-=orderRow.item.price
        order.items.remove(orderRow)
        orderRow.delete()
        if len(order.items)==0:
            order.delete()
        