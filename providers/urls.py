from django.urls import path

from providers.views import (
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    supplier_list,
    SupplierView,
    SupplierDetailView,
    supplier_detail,

)


app_name = 'providers'
urlpatterns = [
    path('', supplier_list, name='list-of-supplier'),
    path('list/', SupplierListView.as_view(), name='supplier_list'),
    path('create/', SupplierCreateView.as_view(), name='create'),
    path('follow/', SupplierView, name='supplier-home'),
    path('(<slug:slug>)/', SupplierUpdateView.as_view(), name='supplier-detail'),
    # path('(<slug:slug>)/', SupplierDetailView.as_view(), name='detail'),
    path('(<slug:slug>)/', supplier_detail, name='detail'),

]
