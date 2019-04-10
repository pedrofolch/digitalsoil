from django.urls import path
from newsletter.views import control_newsletter,  newsletter_unsubscribe


app_name = 'newsletter'
urlpatterns = [
    path('', control_newsletter, name='control_newsletter'),
    path('unsubscribe/', newsletter_unsubscribe, name='unsubscribe'),
]
