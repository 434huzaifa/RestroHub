from django.db import models
from restaurantSystem.models import Restaurant
# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    def __str__(self) -> str:
        return f'{self.name}'
class Menu(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    items=models.ManyToManyField(Item,blank=True,related_name='menus',)
    
    def __str__(self) -> str:
        return f'{self.restaurant.name}"s Menu'