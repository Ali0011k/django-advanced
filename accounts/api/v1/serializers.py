from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.hashers import make_password


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