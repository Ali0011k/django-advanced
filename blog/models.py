from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from django.utils import timezone
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.BooleanField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    published_time = models.DateTimeField()
    
    def __str__(self):
        return self.title
    
    
    
@receiver(post_save, sender=Category)
def create_first_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            author=User.objects.get(pk = 1),
            category=instance,
            title='first post',
            content='first post content',
            status=True,
            published_time=timezone.now(),
        )