from django.urls import path
# from django.contrib import admin

from labsoil.views import (
    labsoil_list,
    labsoil_create,
    labsoil_detail,
    labsoil_update,
    labsoil_delete,
    lab_soil_result
    )


app_name = 'labsoil'
urlpatterns = [
    path('', labsoil_list, name='list'),
    path('create/', labsoil_create, name='create'),
    path('(<slug:slug>)/', labsoil_detail, name='detail'),
    path('(<slug:slug>)/edit/', labsoil_update, name='update'),
    path('(<slug:slug>)/delete/', labsoil_delete, name='delete'),
    path('(<slug:slug>)/result/', lab_soil_result, name='result'),

    # path('posts/', "<appname>.views.<function_name>"),
]
