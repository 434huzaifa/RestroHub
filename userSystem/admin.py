from django.contrib import admin
from .models import *
from api.admin import ExtendAdmin
# Register your models here.

admin.site.register(Profile,ExtendAdmin)
admin.site.register(Owner,ExtendAdmin)
admin.site.register(Employee,ExtendAdmin)
