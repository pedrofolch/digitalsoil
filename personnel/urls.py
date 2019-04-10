from django.urls import path

from .views import (asset_create,
                    asset_detail,
                    asset_list,
                    asset_update,
                    asset_delete,
                    AssetDetailView
                    )


app_name = 'assets'
urlpatterns = [
    path('', asset_list, name='list'),
    path('create/', asset_create, name='create'),
    # path('(<slug:slug>)/', AssetDetailView.as_view(), name='detail'),
    path('(<slug:slug>)/', asset_detail, name='detail'),
    path('(<slug:slug>)/edit/', asset_update, name='update'),
    path('(<slug:slug>)/delete/', asset_delete, name='delete'),
    # path('asset/', "asset_view.views.<function_name>"),
]
