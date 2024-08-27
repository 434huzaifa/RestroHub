from django.db import models
from restaurantSystem.models import Restaurant
# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    description=models.TextField(blank=True,null=True,default=None)
    def __str__(self) -> str:
        return f'{self.name}'
class Menu(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    items=models.ManyToManyField(Item,blank=True,related_name='menus',)
    
    def __str__(self) -> str:
        return f'{self.name}'