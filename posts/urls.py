from django.urls import path, re_path
# from django.contrib import admin

from posts.views import (
    post_list,
    post_create,
    post_detail,
    post_update,
    post_delete,
    PostDetailView,


    )


app_name = 'posts'
urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create, name='create'),
    # path('(<slug:slug>)/', PostDetailView.as_view(), name='detail'),
    path('(<slug:slug>)/', post_detail, name='detail'),
    path('(<slug:slug>)/edit/', post_update, name='update'),
    path('(<slug:slug>)/delete/', post_delete, name='delete'),
    # path('posts/', "<appname>.views.<function_name>"),

]
