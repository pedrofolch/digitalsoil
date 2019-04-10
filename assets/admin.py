from django.contrib import admin

from .models import TypeOfAsset, MarineVessel, Automobile, Equipment, Asset, Parts, MarineVesselManufacturer, \
    MarineModelType, CarManufacturer, CarModelType, EquipmentManufacturer, EquipmentModelType, ThroughHull, \
    HeavyEquipmentManufacturer, HeavyEquipmentModelType
# Register your models here.


admin.site.register(TypeOfAsset)
admin.site.register(MarineVessel)
admin.site.register(Automobile)
admin.site.register(Equipment)
admin.site.register(Asset)
admin.site.register(Parts)
admin.site.register(HeavyEquipmentManufacturer)
admin.site.register(HeavyEquipmentModelType)
admin.site.register(MarineVesselManufacturer)
admin.site.register(MarineModelType)
admin.site.register(CarModelType)
admin.site.register(CarManufacturer)
admin.site.register(EquipmentManufacturer)
admin.site.register(EquipmentModelType)
admin.site.register(ThroughHull)
