from accounts.models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import *
from accounts.api.v1.serializers import *
from accounts.api.v1.permissions import IsAdminOrOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class UserModelViewSet(ModelViewSet):
    """ a model view set for user model """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['is_active', 'is_staff', 'is_superuser']
    search_fields = ['email']
    ordering_fields = ['id', 'is_active', 'is_staff', 'is_superuser']
    

class ProfileModelViewSet(ModelViewSet):
    """ a model view set for profile model """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['user', 'first_name', 'last_name']
    ordering_fields = ['id']