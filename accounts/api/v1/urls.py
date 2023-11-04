from django.urls import path, include
from accounts.api.v1.views import *
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('user', UserModelViewSet, basename='user')
router.register('profile', ProfileModelViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls), name='accounts-urls'),
    path('get_auth_token/', CustomGetAuthToken.as_view()),
    path('update_auth_token/', UpdateAuthToken.as_view()),
    
]