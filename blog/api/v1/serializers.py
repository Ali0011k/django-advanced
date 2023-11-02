from rest_framework import serializers
from blog.models import *
from accounts.models import Profile

# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255,)


class CategorySerializer(serializers.ModelSerializer):
    """ a serializer for category model """
    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    """ a serializer for post model """
    short_content = serializers.URLField(source='get_content_shorted', read_only=True)
    category = CategorySerializer()
    class Meta:
        model = Post
        
        fields = [
            'id',
            'title',
            'short_content',
            'content',
            'image',
            'author',
            'category',
            'status',
            'published_at'
        ]
        
        read_only_fields = ['author', 'short_content']
        
    
    def to_representation(self, instance):
        pre = super().to_representation(instance)
        request = self.context.get('request')
        if request.parser_context.get('kwargs'):
            pre.pop('short_content')
        else:
            pre.pop('content')
        
        return pre    
    
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user.id
        return super().create(validated_data)
    
    