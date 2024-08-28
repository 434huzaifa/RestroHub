from django.db import models
from menuSystem.models import Item
from restaurantSystem.models import Restaurant
# Create your models here.

class OrderRow(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    
    def __str__(self) -> str:
        return f'{self.id} | {self.item.name} | {self.quantity}'
    
class Order(models.Model):
    restaurant=models.ForeignKey(Restaurant,related_name="restaurant",on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderRow,related_name="orders",blank=True)
    totalPrice=models.FloatField(default=0)
    name=models.CharField(max_length=100,null=True,default=None)
    phone=models.CharField(max_length=15)
    description=models.TextField(default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.id} | {self.name}'
    