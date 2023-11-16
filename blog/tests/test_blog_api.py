from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from decouple import config
import pytest
from accounts.models import *
from blog.models import *


@pytest.fixture
def create_user():
    user = User.objects.create(
        email=config("EMAIL", cast=str),
        password="t@123456",
        is_superuser=True,
        is_staff=True,
        is_active=True,
        is_verified=True,
    )
    return user


@pytest.mark.django_db
class TestPostApi:
    """testing blog api"""

    client = APIClient()

    def test_get_post_list_response(self):
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_401_status(self, create_user):
        """tests create post without user"""
        user = create_user
        self.category = Category.objects.create(name="testCategory")
        url = reverse("blog:api-v1:post-list")
        data = {
            "author": Profile.objects.get(user=user),
            "category": self.category,
            "title": "testing api",
            "content": "this is first post for testing api",
            "status": True,
            "published_at": timezone.now(),
        }
        response = self.client.post(url, data)
        assert response.status_code == 401

    def test_create_post_201_status(self, create_user):
        """testing a post created in db or not"""
        user = create_user
        self.client.force_authenticate(user)
        self.category = Category.objects.create(name="testCategory")
        url = reverse("blog:api-v1:post-list")
        data = {
            "title": "testing apis",
            "content": "this is first post for testing api",
            "status": True,
            "published_at": timezone.now(),
            "category": self.category.id,
        }
        response = self.client.post(url, data, format="json")
        assert response.status_code == 201
