from .views import (
    LabPostRudView, LabPostAPIView
)
from django.urls import path


app_name = 'api-labsoil'
urlpatterns = [
    path('', LabPostAPIView.as_view(), name='lab-list_create'),
    path('(<int:pk>)', LabPostRudView.as_view(), name='lab-rud'),

]
