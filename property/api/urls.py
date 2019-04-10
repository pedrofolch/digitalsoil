from .views import AssetRudView, AssetAPIView
from django.urls import path


app_name = 'api-assets'
urlpatterns = [
    path('', AssetAPIView.as_view(), name='asset-list_create'),
    path('(<slug:slug>)', AssetRudView.as_view(), name='asset-rud'),

]
