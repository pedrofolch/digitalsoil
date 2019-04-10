from .views import PurchaseAPIView, PurchaseRudView
from django.urls import path


app_name = 'api-purchase'
urlpatterns = [
    path('', PurchaseAPIView.as_view(), name='create'),
    path('(<slug:slug>)', PurchaseRudView.as_view(), name='rud'),
]
