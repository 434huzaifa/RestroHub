from django.shortcuts import redirect
from api.utils import code400and500
from api.schema import MessageSchema
from ninja_extra import api_controller, route
from api.utils import AuthCookie
from orderSystem.models import Order
from icecream import ic
import stripe
from os import getenv
from dotenv import load_dotenv
from paymentSystem.schema import *
from paymentSystem.models import *
from api.permission import OwnerOrEmployeeCheck
# Create your views here.
load_dotenv()




@api_controller("/payment", tags=["Payment"], auth=AuthCookie(False))
class PaymentAPI:
    @route.get("", response={200: UrlSchema, code400and500: MessageSchema},description="Response will have a generated link. you can enter the link in browser address without quotation mark to use the link. You will need internet connection",summary="Stripe checkout API")
    def checkout(self, request, order_id: int):
        stripe.api_key = getenv("STRIPE_SEC_KEY")
        order = Order.objects.get(id=order_id)
        if OwnerOrEmployeeCheck(order.restaurant,request):
            t_lite_items = []
            for i in order.items.filter():
                t_items = {
                    "price_data": {
                        "unit_amount": int(round(i.item.price, 2) * 100),
                        "product_data": {
                            "name": i.item.name,
                            "description": {i.item.description},
                        },
                        "currency": "bdt",
                    },
                    "quantity": i.quantity,
                }
                t_lite_items.append(t_items)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=t_lite_items,
                mode="payment",
                customer_creation="always",
                success_url="http://127.0.0.1:8000/payment/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://127.0.0.1:8000/payment/cancel?session_id={CHECKOUT_SESSION_ID}",
                currency="bdt",
                metadata={"order_id": order_id},
                custom_fields=[
                    {
                        "key":"customer_name",
                        "label":{
                            "custom":"Customer Name",
                            "type":"custom"
                        },
                        "type":"text",
                        "text":{
                            "default_value":order.name
                        }
                    },
                    {
                        "key":"customer_phone",
                        "label":{
                            "custom":"Customer Phone",
                            "type":"custom"
                        },
                        "type":"text",
                        "text":{
                            "default_value":order.phone
                        }
                    },
                    {
                        "key":"customer_description",
                        "label":{
                            "custom":"Customer Description",
                            "type":"custom"
                        },
                        "type":"text",
                        "text":{
                            "default_value":order.description
                        }
                    }

                ]
            )
            return 200, {"url":checkout_session.url}
        return 400, {"message": "Owner or Employee mismatch with Restaurant"}
    
    @route.get("/success",response={200:PaymentSchema,code400and500:MessageSchema},description="Generally this should a frontend route. But...",summary="Stripe checkout success route")
    def success(self,request,session_id:str):
        if session_id:
            stripe.api_key = getenv("STRIPE_SEC_KEY")
            session = stripe.checkout.Session.retrieve(session_id)
            order=Order.objects.get(id=int(session.metadata.get('order_id')))
            payment=Payment(order=order,payment_id=session.id,email=session.customer_email,amount=session.amount_total,status="Paid")
            payment.save()
            return 200,payment
        return 400,{"message":"Invalid Sessionid"}
    
    @route.get("/cancel",description="Generally this should a frontend route. But...",summary="Stripe checkout cancel/not paid route")
    def cancel(self,request,session_id:str):
        if session_id:
            stripe.api_key = getenv("STRIPE_SEC_KEY")
            session = stripe.checkout.Session.retrieve(session_id)
            order=Order.objects.get(id=int(session.metadata.get('order_id')))
            payment=Payment(order=order,payment_id=session.id,email=session.customer_email,amount=session.amount_total,status="Unpaid")
            payment.save()
            return 200,{"message":"See you again"}
        return 400,{"message":"Invalid Sessionid"}