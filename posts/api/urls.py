from .views import BlogPostRudView, BlogPostAPIView
from posts.views import PostDetailAPIView
from django.urls import path, re_path


app_name = 'api-posts'
urlpatterns = [
    path('', BlogPostAPIView.as_view(), name='post-listcreate'),
    path('(<int:pk>)', BlogPostRudView.as_view(), name='post-rud'),
    re_path(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail'),

]
