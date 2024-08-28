from django.db import models
from orderSystem.models import Order
# Create your models here.

class Payment(models.Model):
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    payment_id=models.CharField(max_length=100)
    amount=models.FloatField()
    email=models.EmailField(blank=True,null=True)
    status=models.CharField(max_length=15,choices=models.TextChoices("status",("Paid Unpaid")))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    