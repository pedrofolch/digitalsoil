from django.urls import path, re_path
# from django.contrib import admin

from iotsensor.views import (
    sensoriot_list,
    sensoriot_create,
    # post_detail,
    sensoriot_update,
    sensoriot_delete,
    SensorIoTDetailView,

    )


app_name = 'iotsensor'
urlpatterns = [
    path('', sensoriot_list, name='list'),
    path('create/', sensoriot_create, name='create'),
    path('(<slug:slug>)/', SensorIoTDetailView.as_view(), name='detail'),
    path('(<slug:slug>)/edit/', sensoriot_update, name='update'),
    path('(<slug:slug>)/delete/', sensoriot_delete, name='delete'),
    # path('posts/', "<appname>.views.<function_name>"),

]
