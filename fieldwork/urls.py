from django.urls import path

from fieldwork.views import (
    field_work_create,
    FieldWorkListView,
    AllUserRecentFieldWorkListView,
    FieldWorkDetailView,
    fieldwork_update,
    fieldwork_average,
    fieldwork_detail,
)


app_name = 'fieldwork'
urlpatterns = [
    path('', FieldWorkListView.as_view(), name='fieldwork_list'),
    path('create/', field_work_create, name='create'),
    path('list', AllUserRecentFieldWorkListView.as_view(), name='list'),
    path('(<slug:slug>)/', fieldwork_detail, name='fieldwork_detail'),
    # path('(<slug:slug>)/', FieldWorkDetailView, name='fieldwork_detail'),
    path('(<slug:slug>)/edit/', fieldwork_update, name='action'),
    # path('average/(<slug:slug>)', average_create, name='average_data'),
    path('(<slug:slug>)/average/', fieldwork_average, name='average'),

]
