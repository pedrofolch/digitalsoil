from .views import FuelStationAPIView, FuelStationRudView
from django.urls import path


app_name = 'api-fuel_station'
urlpatterns = [
    path('', FuelStationAPIView.as_view(), name='create'),
    path('(<slug:slug>)', FuelStationRudView.as_view(), name='fuel-rud'),
]
