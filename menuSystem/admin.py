from django.contrib import admin
from api.admin import ExtendAdmin
from menuSystem.models import *
# Register your models here.


admin.site.register(Item,ExtendAdmin)
admin.site.register(Menu,ExtendAdmin)