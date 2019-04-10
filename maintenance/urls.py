from django.urls import path
# from django.contrib import admin

from .views import (
    schedules,
    schedule_list,
    schedule_create,
    # schedule_detail,
    # schedule_update,
    # schedule_delete,
    )


app_name = 'maintenance'
urlpatterns = [
    path('', schedules, name='schedules'),
    path('list', schedule_list, name='list'),
    path('create/', schedule_create, name='create'),
    # path('(<slug>)/', schedule_detail, name='detail'),
    # path('(<slug>)/edit/', schedule_update, name='update'),
    # path('(<slug>)/delete/', schedule_delete, name='delete'),
    # path('posts/', "<appname>.views.<function_name>"),
]
