from django.urls import path, include
from accounts.api.v1.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'api-v1'

router = DefaultRouter()
router.register('user', UserModelViewSet, basename='user')
router.register('profile', ProfileModelViewSet, basename='profile')


urlpatterns = [
    path('', include(router.urls), name='accounts-urls'),
    
    # token authentication
    path('get_auth_token/', CustomGetAuthToken.as_view()),
    path('update_auth_token/', UpdateAuthToken.as_view()),
    
    # jwt authentication
    # path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/create/', CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    
    # change password
    path('change_password/', ChangePassword.as_view(), name='change-password'),
    
    path('test-email/', SendTestEmail.as_view(), name='console-email'),
    
    # verify email
    path('send-verification-email/', SendVerificationEmailApiView.as_view(), name='send-verification-email'),
    path('verify-account/<str:token>', VerifyAccount.as_view(), name='verify-account')
]