from .views import RecipeRudView, RecipeAPIView
from django.urls import path


app_name = 'api-recipes'
urlpatterns = [
    path('', RecipeAPIView.as_view(), name='pileofcompost-listcreate'),
    path('(<slug:slug>)', RecipeRudView.as_view(), name='pileofcompost-rud'),
]
