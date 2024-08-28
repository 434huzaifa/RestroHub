from django.db import models
from menuSystem.models import Menu

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    menus=models.ManyToManyField(Menu,related_name="restaurants")
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True,default=None)
    opening_hours = models.TimeField(blank=True, null=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id} | {self.name}'
