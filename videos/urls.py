from django.urls import path

from .views import video_detail, category_list, category_detail


app_name = 'videos'
urlpatterns = [
    path('', category_list, name='projects'),
    path('(<username>)/', video_detail, name='detail'),
    path('<cat_slug>/', category_detail, name='project_detail'),
    path('<cat_slug>/<vid_slug>/', video_detail, name='video_detail')
]
