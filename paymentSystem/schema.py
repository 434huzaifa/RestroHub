from ninja import Schema,ModelSchema
from paymentSystem.models import *
class UrlSchema(Schema):
    url:str
    
class PaymentSchema(ModelSchema):
    class Meta:
        model=Payment
        fields='__all__'
        exclude=['id']
