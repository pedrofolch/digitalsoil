from .views import ProductRudView, ProductAPIView
from products.views import ProductDetailAPIView
from django.urls import path, re_path


app_name = 'api-products'
urlpatterns = [
    path('', ProductAPIView.as_view(), name='product-list_create'),
    path('(<int:pk>)', ProductRudView.as_view(), name='product-rud'),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailAPIView.as_view(), name='detail'),

]
