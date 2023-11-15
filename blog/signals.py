from django.dispatch import receiver
from django.db.models.signals import post_save
from decouple import config
from blog.models import *
from django.utils import timezone
from accounts.models import *


# a signal for create a post when category is created
@receiver(post_save, sender=Category)
def create_first_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            author=Profile.objects.get(
                user=User.objects.get(email=config("EMAIL", cast=str))
            ),
            category=instance,
            title=f"first post for {instance} category",
            content=f"this is first post for {instance} category",
            status=True,
            published_at=timezone.now(),
        )
