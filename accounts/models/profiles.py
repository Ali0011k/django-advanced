from django.db import models
from django.contrib.auth.models import *
from .users import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    bio = models.TextField(default="")

    def __str__(self):
        return self.user.email
