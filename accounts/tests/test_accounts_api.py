from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from decouple import config
from accounts.models import *


class TestProfileApi(TestCase):
    """testing profile apis"""

    def setUp(self):
        """setting up test's requirements (objects are created in test runner in core of project)"""
        self.client = APIClient()
        self.user = User.objects.get(email=config("EMAIL", cast=str))
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_list_of_objects_200_response(self):
        """testing profile list's response's status code"""
        url = reverse("accounts:api-v1:profile-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_profile_created_object(self):
        """testing profile is created (profile is creating by signals when user is created)"""
        self.assertTrue(self.profile)

    def test_profile_equals(self):
        """testing profile is equals"""
        self.assertEqual(self.profile.user, self.user)


class TestUserApi(TestCase):
    """testing user apis"""

    def setUp(self):
        """setting up test's requirements (objects are created in test runner in core of project)"""
        self.client = APIClient()
        self.user = User.objects.get(email=config("EMAIL", cast=str))
        self.profile = Profile.objects.get(user=self.user)

    def test_user_list_of_objects_200_response(self):
        """testing profile list's response's status code"""
        url = reverse("accounts:api-v1:user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_and_profile_are_creating(self):
        """testing user and user's profile are creating or not"""
        url = reverse("accounts:api-v1:user-list")
        data = {
            "email": "test@test.com",
            "password": "t@123456",
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
            "is_verified": True,
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format="json")
        profile = User.objects.get(email="test@test.com")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(profile)

    def test_create_user_with_out_authentication(self):
        """testing user creation with out authentication"""
        url = reverse("accounts:api-v1:user-list")
        data = {
            "email": "test@test.com",
            "password": "t@123456",
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
            "is_verified": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_user_with_invalid_data(self):
        """testing user creation with invalid data"""
        url = reverse("accounts:api-v1:user-list")
        data = {
            "password": "t@123456",
            "is_superuser": True,
            "is_staff": True,
            "is_active": True,
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_user_token(self):
        """testing user's token"""
        token = Token.objects.get(user=self.user)
        self.assertEqual(self.user.auth_token, token)
