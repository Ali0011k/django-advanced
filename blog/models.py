from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from accounts.models import User
from django.utils import timezone
from accounts.models import Profile


class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.BooleanField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    published_time = models.DateTimeField()
    
    def __str__(self):
        return self.title
    
    def get_content_shorted(self):
        return str(self.content[0:10])
    
@receiver(post_save, sender=Category)
def create_first_post(sender, instance, created, **kwargs):
    if created:
        Post.objects.create(
            author=Profile.objects.get(user = User.objects.get(email = 'kly441781@gmail.com')),
            category=instance,
            title='first post',
            content='first post content',
            status=True,
            published_time=timezone.now(),
        )