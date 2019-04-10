from django.urls import path

from .views import (
                    repair_create,
                    repair_detail,
                    repair_list,
                    repair_update,
                    repair_delete,
                    repair_order_create,
                    repair_order_detail,
                    repair_order_list,
                    repair_order_update,
                    repair_order_delete,
                    )


app_name = 'repairs'
urlpatterns = [
    path('', repair_list, name='list'),
    path('create/', repair_create, name='create'),
    path('(<slug:slug>)/', repair_detail, name='detail'),
    path('(<slug:slug>)/edit/', repair_update, name='update'),
    path('(<slug:slug>)/delete/', repair_delete, name='delete'),

    path('order/', repair_order_list, name='repair_order_list'),
    path('order/create/', repair_order_create, name='repair_order_create'),
    path('order/(<slug:slug>)/', repair_order_detail, name='repair_order_detail'),
    path('order/(<slug:slug>)/edit/', repair_order_update, name='repair_order_update'),
    path('order/(<slug:slug>)/delete/', repair_order_delete, name='repair_order_delete'),

]
