from django.urls import path
# from django.contrib import admin

from recipes.views import (
    RecipeCreateView,
    RecipeUpdateView,
    AllUserRecentRecipeListView,
    RecipeListView,
    recipe_list,
    recipe_detail,
    # HomeView
    )


app_name = 'recipes'
urlpatterns = [
    path('', RecipeListView.as_view(), name='recipe_list'),
    path('(<slug:slug>[\w-]+)/', RecipeUpdateView.as_view(), name='detail'),
    path('all/', AllUserRecentRecipeListView.as_view(), name='all'),
    path('edit/',  RecipeCreateView.as_view(), name='create'),
    path('list/', recipe_list, name='list-all'),
    # path('follow/', HomeView.as_view(), name='home-feed'),
    # path('(<slug:slug>)/', recipe_detail, name='detail'),
    # path('(<slug:slug>)/delete/', recipe_delete, name='delete'),

]
