from django.db import models

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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField()
    
    def __str__(self):
        return self.title
    
    def get_content_shorted(self):
        return str(self.content[0:10])



