from .views import FieldWorkRudView, FieldWorkAPIView
from django.urls import path


app_name = 'api-fieldwork'
urlpatterns = [
    path('', FieldWorkAPIView.as_view(), name='fieldwork-list_create'),
    path('(<int:pk>)', FieldWorkRudView.as_view(), name='field-rud'),

]
