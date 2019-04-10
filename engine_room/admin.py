from django.contrib import admin

from .models import Engines, MainEngine, \
    CenterEngine, PortEngine, \
    PortEngine2, PortEngine3, \
    StarboardEngine, StarboardEngine2, \
    StarboardEngine3, Auxiliary, GenSet, GenSet2, Tools

# Register your models here.


admin.site.register(Engines)
admin.site.register(MainEngine)
admin.site.register(CenterEngine)
admin.site.register(PortEngine)
admin.site.register(PortEngine2)
admin.site.register(PortEngine3)
admin.site.register(StarboardEngine)
admin.site.register(StarboardEngine2)
admin.site.register(StarboardEngine3)
admin.site.register(Auxiliary)
admin.site.register(GenSet)
admin.site.register(GenSet2)
admin.site.register(Tools)
