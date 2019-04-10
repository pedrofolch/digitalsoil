from django.urls import path

from .views import (
    product_list,
    product_create,
    product_update,
    product_delete,
    product_detail

    )


app_name = 'products'

urlpatterns = [
    path('', product_list, name='product_list'),
    path('create/', product_create, name='create'),
    path('(<slug:slug>)/', product_detail, name='detail'),
    path('(<slug:slug>)/edit/', product_update, name='update'),
    path('(<slug:slug>)/delete/', product_delete, name='delete'),

]
