from rest_framework import serializers
from blog.models import *
from accounts.models import Profile

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255,)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """ a serializer for post model """
    short_content = serializers.URLField(source='get_content_shorted', read_only=True)
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'short_content']
        
    
    def to_representation(self, instance):
        pre = super().to_representation(instance)
        request = self.context.get('request')
        if request.parser_context.get('kwargs'):
            pre.pop('short_content')
        pre['category'] = CategorySerializer(instance=instance.category, context={'request':request}).data
        return pre 