from django.urls import re_path

from .views import my_profile

app_name = 'accounts'

urlpatterns = [
	re_path(r'^profile/$', my_profile, name='my_profile')
]
