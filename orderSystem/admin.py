from django.contrib import admin
from api.admin import ExtendAdmin
from orderSystem.models import *
# Register your models here.

admin.site.register(OrderRow,ExtendAdmin)
admin.site.register(Order,ExtendAdmin)