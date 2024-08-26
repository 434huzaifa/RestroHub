from django.db import models
# Create your models here.
class Restaurant(models.Model):
     name = models.CharField(max_length=255)
     address = models.CharField(max_length=255)
     phone_number = models.CharField(max_length=20)
     description = models.TextField(blank=True, null=True)
     opening_hours = models.TimeField(blank=True,null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)
     
     def __str__(self):
        return self.name