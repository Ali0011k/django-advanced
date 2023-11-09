from typing import Any, Dict
from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserSerializer(serializers.ModelSerializer):
    """ a model serailzer for user model """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'is_superuser',
            'is_staff',
            'is_active',
        ]

    
    def create(self, validated_data):
        """ hashing password when user is creating """
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    
    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    """ a model serializer for profile model """
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'image',
            'bio'
        ]


    # def to_representation(self, instance):
    #     pre = super().to_representation(instance)
    #     request = self.context.get('request')
    #     pre['user'] = UserSerializer(instance.user, context={'request':request}).data
    #     return pre
    
    

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({'details':'user is not verified'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ custom serializer for creating or getting an jwt """
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        data['email'] = self.user.email
        return data
    

class ChangePasswordSerializer(serializers.Serializer):
    """ a serializer for changing user's password """
    old_password = serializers.CharField(required = True)
    new_password1 = serializers.CharField(required = True)
    new_password2 = serializers.CharField(required = True)
    
    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise ValidationError({'new_passwords':'passwords are does not match'})
        return super().validate(attrs)