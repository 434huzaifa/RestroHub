from django.db import models
# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    description=models.TextField(blank=True,null=True,default=None)
    def __str__(self) -> str:
        return f'{self.id} | {self.name}'
    
class Menu(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    items=models.ManyToManyField(Item,blank=True,related_name='items')
    
    def __str__(self) -> str:
        return f'{self.id} | {self.name}'