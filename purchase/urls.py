from django.urls import path

from purchase.views import (
    PurchaseListView,
    PurchaseCreateView,
    PurchaseUpdateView,
    purchase_list,
    PurchaseView,
    PurchaseDetailView,
    purchase_detail,

)


app_name = 'purchase'
urlpatterns = [
    path('', purchase_list, name='list'),
    path('list/', PurchaseListView.as_view(), name='supplier_list'),
    path('create/', PurchaseCreateView.as_view(), name='create'),
    path('follow/', PurchaseView, name='supplier-home'),
    path('(<slug:slug>)/', PurchaseUpdateView.as_view(), name='update'),
    # path('(<slug:slug>)/', PurchaseDetailView.as_view(), name='detail'),
    path('(<slug:slug>)/', purchase_detail, name='detail'),

]
