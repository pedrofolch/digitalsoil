from .views import SupplierAPIView, SupplierRudView
from django.urls import path


app_name = 'api-providers'
urlpatterns = [
    path('', SupplierAPIView.as_view(), name='supplier-create'),
    path('(<slug:slug>)', SupplierRudView.as_view(), name='supplier-rud'),
]
