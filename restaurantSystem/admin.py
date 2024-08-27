from django.contrib import admin
from api.admin import ExtendAdmin
from .models import *

# Register your models here.
admin.site.register(Restaurant,ExtendAdmin)
