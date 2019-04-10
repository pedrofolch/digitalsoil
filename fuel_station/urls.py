from django.urls import path

from .views import (
                    fuel_station_create,
                    fuel_station_detail,
                    fuel_station_list,
                    fuel_station_update,
                    fuel_station_delete,
                    )


app_name = 'fuel_station'
urlpatterns = [
    path('', fuel_station_list, name='list'),
    path('create/', fuel_station_create, name='create'),
    path('(<slug:slug>)/', fuel_station_detail, name='detail'),
    path('(<slug:slug>)/edit/', fuel_station_update, name='update'),
    path('(<slug:slug>)/delete/', fuel_station_delete, name='delete'),
]
