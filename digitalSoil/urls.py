from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterView, ProfileFollowToggle, activate_user_view
from iotsensor.views import scrape
# from .views import home_news
from recipes.views import AllUserRecentRecipeListView
from shops import views
# from providers.views import HomeView
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token
from graphene_django.views import GraphQLView
from pages.views import HomeView


urlpatterns = [
    # path('', views.Home.as_view()),

    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_jwt_token, name='api-login'),

    path('profiles/', include('accounts.urls')),
    path('api/products/', include('products.api.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('shopping_cart.urls')),
    path('accounts/', include('allauth.urls')),

    path('api/posts/', include('posts.api.urls')),
    path('posts/', include('posts.urls')),

    path('api/assets/', include('assets.api.urls')),
    path('assets/', include('assets.urls')),

    path('api/sensor/', include('iotsensor.api.urls')),
    path('sensor/', include('iotsensor.urls')),
    path('scrape/', scrape, name='scrape'),
    # path('news/', home_news, name="home_news"),

    path('api/engine_room/', include('engine_room.api.urls')),
    path('engine_room/', include('engine_room.urls')),
    path('api/fuel/', include('fuel_station.api.urls')),
    path('fuel/', include('fuel_station.urls')),
    path('api/repairs/', include('repairs.api.urls')),
    path('repairs/', include('repairs.urls')),

    path('api/orders/', include('purchase.api.urls')),
    path('orders/', include('purchase.urls')),

    path('api/providers/', include('providers.api.urls')),
    path('providers/', include('providers.urls')),

    path('api/recipes/', include('recipes.api.urls')),
    path('recipes/', include('recipes.urls')),

    path('api/labsoil/', include('labsoil.api.urls')),
    path('labsoil/', include('labsoil.urls')),

    path('api/fieldwork/', include('fieldwork.api.urls')),
    path('fieldwork/', include('fieldwork.urls')),
    path('compost/', TemplateView.as_view(template_name="compost.html"), name='compost'),

    path('memberships/', include('memberships.urls', namespace='memberships')),
    path('courses/', include('courses.urls', namespace='courses')),

    path('recent/', AllUserRecentRecipeListView.as_view(), name='recent'),

    path('comments/', include('comments.urls')),
    # path('commentaries/', include('commentaries.urls')),

    path('folch2iot/', TemplateView.as_view(template_name='folch2iot.html'), name='folch2iot'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegisterView.as_view(), name='registration'),
    path('activate/(<code:[a-z0-9].*)/>', activate_user_view, name='activate'),

    path('profile/follow/', ProfileFollowToggle.as_view(), name='follow'),
    path('register/', RegisterView.as_view(template_name='registration/register.html'), name='register'),

    path('', HomeView.as_view(), name='home'),

    # path('', home_news, name='home'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
