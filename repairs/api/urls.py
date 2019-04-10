from .views import RepairAPIView, RepairRudView, RepairOrderAPIView, RepairOrderRudView
from django.urls import path


app_name = 'api-repairs'
urlpatterns = [
    path('', RepairAPIView.as_view(), name='create'),
    path('(<slug:slug>)', RepairRudView.as_view(), name='repair-rud'),
    path('order/', RepairOrderAPIView.as_view(), name='create'),
    path('order/(<slug:slug>)', RepairOrderRudView.as_view(), name='repair_order-rud'),
]
