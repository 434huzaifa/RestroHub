from icecream import ic
from ninja import PatchDict
from ninja_extra import api_controller, route

from api.schema import MessageSchema
from api.utils import AuthCookie, code400and500
from orderSystem.schema import *
from orderSystem.models import *
from restaurantSystem.models import Restaurant
from api.permission import OwnerOrEmployeeCheck

# Create your views here.


@api_controller("/order", tags=["Order"], auth=AuthCookie(False))
class OrderAPI:
    @route.post(
        "",
        response={201: OrderSchema, code400and500: MessageSchema},
        summary="Create order with multiple items at once",
    )
    def create_order(self, request, body: OrderCreateSchema):
        data = body.model_dump()
        restaurant = Restaurant.objects.get(id=data.get("restaurant_id"))
        if OwnerOrEmployeeCheck(restaurant, request):
            menu = restaurant.menus.get(id=data.get("menu_id"))
            orderRows = []
            t_totalPrice = 0.0
            for i in data.get("items"):
                item = menu.items.get(id=i.get("item_id"))
                orderRow = OrderRow(item=item, quantity=i.get("quantity"))
                orderRow.save()
                t_totalPrice += i.get("quantity") * item.price
                orderRows.append(orderRow)

            order = Order(
                totalPrice=t_totalPrice, restaurant=restaurant, phone=data.get("phone")
            )
            if data.get("name", None):
                order.name = data.get("name")
            if data.get("description", None):
                order.description = data.get("description")
            order.save()
            order.items.set(orderRows)
            return 201, order
        return 400, {"message": "Owner or Employee mismatch with Restaurant"}

    @route.patch(
        "",
        response={201: OrderWithoutItemsSchema, code400and500: MessageSchema},
        summary="Update name, phone or description of order",
    )
    def update_order(self, request, body: PatchDict[OrderUpdateSchema], order_id: int):
        order = Order.objects.get(id=order_id)
        if OwnerOrEmployeeCheck(order.restaurant, request):
            for key, value in body.items():
                setattr(order, key, value)
            order.save()
            return 201, order
        return 400, {"message": "Owner or Employee mismatch with Restaurant"}

    @route.delete(
        "",
        response={200: MessageSchema, code400and500: MessageSchema},
        summary="Delete an order",
    )
    def delete_order(self, request, order_id: int):
        order = Order.objects.get(id=order_id)
        if OwnerOrEmployeeCheck(order.restaurant, request):
            message = f'{order.name}"s order has been deleted'
            order.delete()
            return 200, {"message": message}

    @route.post(
        "/single",
        response={201: OrderSchema, code400and500: MessageSchema},
        summary="Add single items to existing order ",
    )
    def add_single_order(self, request, body: SingleOrderCreateSchema):
        data = body.model_dump()
        order = Order.objects.get(id=data.get("order_id"))
        if OwnerOrEmployeeCheck(order.restaurant, request):
            menu = order.restaurant.menus.get(id=data.get("menu_id"))
            item = menu.items.get(id=data.get("item_id"))
            orderRow = OrderRow(item=item, quantity=data.get("quantity"))
            orderRow.save()
            order.totalPrice += data.get("quantity") * item.price
            order.items.add(orderRow)
            order.save()
            return 400, {"message": "Item does not belong to the restaurant"}
        return 400, {"message": "Owner or Employee mismatch with Restaurant"}

    @route.delete(
        "/item",
        response={200: MessageSchema, code400and500: MessageSchema},
        summary="Delete an item from a order",
    )
    def delete_item(self, request, items_id: int, order_id: int):
        order = Order.objects.get(id=order_id)
        if OwnerOrEmployeeCheck(order.restaurant, request):
            orderRow = OrderRow.objects.get(id=items_id)
            order.totalPrice -= orderRow.item.price
            order.items.remove(orderRow)
            orderRow.delete()
            if order.items.count() == 0:
                order.delete()
        return 400, {"message": "Owner or Employee mismatch with Restaurant"}
