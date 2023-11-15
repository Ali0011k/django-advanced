from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from decouple import config
import pytest
from accounts.models import *
from blog.models import *


@pytest.mark.django_db
class TestPostApi:
    """testing blog api"""

    client = APIClient()

    def test_get_post_list_response(self):
        url = reverse("blog:api-v1:post-list")
        response = self.client.get(url)
        assert response.status_code == 200

    def test_create_post_401_status(self):
        user = User.objects.create(
            email=config("EMAIL", cast=str),
            password=config("DJANGO_SUPERUSER_PASSWORD", cast=str),
            is_superuser=True,
            is_staff=True,
            is_active=True,
            is_verified=True,
        )
        profile = Profile.objects.create(user=user)
        category = Category.objects.create("test")
        url = reverse("blog:api-v1:post-list")
        data = {
            "author": profile,
            "category": category,
            "image": None,
            "title": "testing api",
            "content": "this is first post for testing api",
            "status": True,
            "published_at": timezone.now(),
        }
        response = self.client.post(url, data)
        assert response.status_code == 401
