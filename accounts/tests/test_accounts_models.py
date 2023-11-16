from django.test import TestCase
from decouple import config
from accounts.models import *


class TestUserModel(TestCase):
    """testing User model"""

    def setUp(self):
        """setting up test's requirements (objects are created in test runner in core of project)"""
        self.user = User.objects.get(email=config("EMAIL", cast=str))

    def test_user_is_created(self):
        """testing user is created or not"""
        self.assertTrue(self.user)

    def test_user_equals(self):
        """testing user informations"""
        self.assertEqual(self.user.email, config("EMAIL", cast=str))


class TestProfileModel(TestCase):
    """testing Profile model"""

    def setUp(self):
        """setting up test's requirements (objects are created in test runner in core of project)"""
        self.user = User.objects.get(email=config("EMAIL", cast=str))
        self.profile = Profile.objects.get(user=self.user)

    def test_profile_exists(self):
        """testing user is exists"""
        self.assertTrue(self.profile)

    def test_profile_equals(self):
        self.assertEqual(self.profile.user, self.user)
