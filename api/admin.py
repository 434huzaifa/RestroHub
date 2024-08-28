from django.contrib import admin


class ExtendAdmin(admin.ModelAdmin):
    list_display = ["__str__", "id"]
