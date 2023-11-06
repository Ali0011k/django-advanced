from accounts.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *
from rest_framework.filters import OrderingFilter, SearchFilter
from accounts.api.v1.serializers import *
from accounts.api.v1.permissions import IsAdminOrOwner
from accounts.api.v1.paginations import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
class UserModelViewSet(ModelViewSet):
    """ a model view set for user model """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
    ordering_fields = ['id', 'is_active', 'is_staff', 'is_superuser']
    pagination_class = UserPagination
    
    


class ProfileModelViewSet(ModelViewSet):
    """ a model view set for profile model """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['user', 'first_name', 'last_name']
    ordering_fields = ['id']
    pagination_class = ProfilePagination
    
    
class CustomGetAuthToken(ObtainAuthToken):
    """ a custom view for see user's token and create a new token (for know it see the inheritances)"""
    
    serializer_class = CustomAuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'email' : user.email,
            'token' : token.key
        })
        

class UpdateAuthToken(APIView):
    """ delete users token and replace it with a new token """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'email' : user.email,
            'token' : token.key
        })
        

class CustomTokenObtainPairView(TokenObtainPairView):
    """ custom jwt view for getting or creating jwt tokens for user"""
    serializer_class = CustomTokenObtainPairSerializer
        

class ChangePassword(generics.GenericAPIView):
    """ a view for change user's password """
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def get_object(self):
        """ get user from request instead of queryparams id """
        obj = self.request.user
        return obj
    
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        self.object = self.get_object()
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                raise ValidationError({'old_password':'password does not correct'})
            try:
                validate_password(serializer.data.get('new_password1'))
            except DjangoValidationError as e:
                return Response(list(e.messages))
            self.object.set_password(serializer.data.get('new_password1'))
            self.object.save()
            return Response({
                'detail':'password reset successfuly'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)