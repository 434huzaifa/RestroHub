from django.db import models
from django.contrib.auth.models import User
from restaurantSystem.models import Restaurant

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, default=None, null=True)
    address = models.TextField(default=None, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class Owner(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    restaurants = models.ManyToManyField(Restaurant, related_name="owners")

    def __str__(self):
        return f"{self.profile.name}"


class Employee(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="employees"
    )

    def __str__(self):
        return f"{self.profile.name}"
