from .views import AssetRudView, AssetAPIView, MarineAssetAPIView, MarineAssetRudView, \
    LandAssetAPIView, LandAssetRudView, \
    EquipmentAssetAPIView, EquipmentAssetRudView, \
    AssetAssetAPIView, AssetAssetRudView, \
    PartsAPIView, PartsRudView, \
    CarManufacturerAPIView, CarManufacturerRudView, \
    MarineVesselManufacturerSerializerAPIView, MarineVesselManufacturerRudView, \
    EquipmentManufacturerAPIView, EquipmentManufacturerRudView, \
    CarModelTypeAPIView, CarModelTypeRudView, MarineModelTypeAPIView, MarineModelTypeRudView, \
    EquipmentModelTypeAPIView, EquipmentModelTypeRudView, \
    ThroughHullAPIView, ThroughHullRudView

from django.urls import path, re_path

app_name = 'api-assets'
urlpatterns = [
    path('', AssetAPIView.as_view(), name='asset-list_create'),

    path('(<slug:slug>)', AssetRudView.as_view(), name='asset-rud'),

    re_path('asset/', AssetAssetAPIView.as_view(),
            name='asset_detail'),
    re_path('asset/(?P<pk>\d+)/', AssetAssetRudView.as_view(),
            name='asset-rud'),

    re_path('parts/', PartsAPIView.as_view(),
            name='part_detail'),
    re_path('parts/(?P<pk>\d+)/', PartsRudView.as_view(),
            name='asset-marine-parts-rud'),

    re_path('equipment/', EquipmentManufacturerAPIView.as_view(),
            name='equipment-manufacturer_detail'),
    re_path('equipment/(?P<pk>\d+)/', EquipmentManufacturerRudView.as_view(),
            name='asset-equipment-manufacturer-rud'),

    re_path('equipment/model', EquipmentModelTypeAPIView.as_view(),
            name='equipment-model_detail'),
    re_path('equipment/model/(?P<pk>\d+)/', EquipmentModelTypeRudView.as_view(),
            name='asset-equipment-model-rud'),

    re_path('through_hull/', ThroughHullAPIView.as_view(),
            name='through-hull_detail'),
    re_path('asset/(?P<pk>\d+)/', ThroughHullRudView.as_view(),
            name='asset-marine-through-hull-rud'),

    path('marine/', MarineAssetAPIView.as_view(), name='asset-marine-list_create'),
    path('marine/(<slug:slug>)', MarineAssetRudView.as_view(), name='asset-marine-rud'),

    re_path('marine/manufacturer/', MarineVesselManufacturerSerializerAPIView.as_view(),
            name='marine-manufacturer_detail'),
    re_path('marine/manufacturer/(?P<pk>\d+)/', MarineVesselManufacturerRudView.as_view(),
            name='asset-marine-manufacturer-rud'),

    re_path('marine/model/', MarineModelTypeAPIView.as_view(),
            name='marine-model_detail'),
    re_path('marine/model/(?P<pk>\d+)/', MarineModelTypeRudView.as_view(),
            name='asset-marine-model-rud'),

    path('land/', LandAssetAPIView.as_view(), name='asset-land-list_create'),
    path('land/(<slug:slug>)', LandAssetRudView.as_view(), name='asset-land-rud'),

    re_path('land/manufacturer/', CarManufacturerAPIView.as_view(),
            name='car-manufacturer_detail'),
    re_path('land/manufacturer/(?P<pk>\d+)/', CarManufacturerRudView.as_view(),
            name='asset-car-manufacturer-rud'),

    re_path('land/model/', CarModelTypeAPIView.as_view(),
            name='car-model_detail'),
    re_path('land/model/(?P<pk>\d+)/', CarModelTypeRudView.as_view(),
            name='asset-car-model-rud'),

    path('equipment/', EquipmentAssetAPIView.as_view(), name='asset-equipment-list_create'),
    path('equipment/(<slug:slug>)', EquipmentAssetRudView.as_view(), name='asset-equipment-rud'),

]
