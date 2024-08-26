from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profiles(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15,default=None,null=True)
    address=models.TextField(default=None,null=True)
    name=models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.name}'