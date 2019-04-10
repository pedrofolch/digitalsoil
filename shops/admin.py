from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Shop, ZipCode, Elevation


@admin.register(Shop)
class ShopAdmin(OSMGeoAdmin):
    list_display = ['location']


admin.site.register(ZipCode)
admin.site.register(Elevation)
