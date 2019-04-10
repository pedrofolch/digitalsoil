from django.urls import path, re_path

from .views import ProfileDetailView, RandomProfileDetailView


app_name = 'profiles'
urlpatterns = [
    path('random/', RandomProfileDetailView.as_view(), name='random'),
    re_path(r'^(?P<username>[^/]+)/$', ProfileDetailView.as_view(), name='detail'),
]
