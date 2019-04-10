from .views import VideoRudView, VideoAPIView
from django.urls import path


app_name = 'api-videos'
urlpatterns = [
    path('', VideoAPIView.as_view(), name='video-listcreate'),
    path('(<int:pk>)', VideoRudView.as_view(), name='video-rud'),
]
