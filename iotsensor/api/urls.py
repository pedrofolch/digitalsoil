from .views import SensorIoTRudView, SensorIoTAPIView
from iotsensor.views import SensorIoTDetailAPIView
from django.urls import path, re_path


app_name = 'api-iotsensor'
urlpatterns = [
    path('', SensorIoTAPIView.as_view(), name='sensor-list_create'),
    path('(<int:pk>)', SensorIoTRudView.as_view(), name='sensor-rud'),
    re_path(r'^(?P<pk>\d+)/$', SensorIoTDetailAPIView.as_view(), name='detail'),

]
