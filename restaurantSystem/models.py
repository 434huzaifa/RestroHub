from django.db import models
from userSystem.models import Profiles
# Create your models here.
class Restaurant(models.Model):
     owner = models.ForeignKey(Profiles, on_delete=models.CASCADE, related_name='owned_restaurants')
     name = models.CharField(max_length=255)
     address = models.CharField(max_length=255)
     phone_number = models.CharField(max_length=20)
     description = models.TextField(blank=True, null=True)
     opening_hours = models.CharField(max_length=100, blank=True, null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
     def __str__(self):
        return self.name