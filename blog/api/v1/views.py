from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.generics import *
from rest_framework import mixins
from rest_framework import viewsets
from blog.api.v1.serializers import *
from blog.models import *
from django.shortcuts import get_object_or_404
from blog.api.v1.permissions import IsOwnerOrReadonly
from blog.api.v1.pagination import PostPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter


# api
# function based

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_view(request):
    if request.method == 'GET':
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_detail_view(request, pk):
    post = get_object_or_404(Post, pk=pk, status=True)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({
            'detail' : 'object has ben deleted'
        },
            status = status.HTTP_204_NO_CONTENT
        )
        
        
# class based views

# class PostListView(APIView):
#     """ retrieving all posts and creating new post """
    
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer
    
#     def get(self, request):
#         """ retrieving all post with True status """
#         posts = Post.objects.filter(status = True)
#         serializer = self.serializer_class(posts, many=True)
#         return Response(serializer.data)
    
    
#     def post(self, request):
#         """ creating a new post """
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
    
    
# class PostDetailView(APIView):
#     """ retrieving a post and delete or update that """
    
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer
    
    
#     def get(self, request, pk):
#         """ retrieving post """
        
#         post = get_object_or_404(Post, pk=pk, status=True)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
    
    
#     def put(self, request, pk):
#         """ updating post """
        
#         post = get_object_or_404(Post, pk=pk, status = True)
#         serializer = self.serializer_class(data=request.data, instance=post)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    
    
#     def delete(self, request, pk):
#         post = get_object_or_404(Post, pk=pk, status=True)
#         post.delete()
#         return Response({
#             'detail' : 'post has been deleted'
#         }, 
#         status=status.HTTP_204_NO_CONTENT
#         )







# generic views

# sample of creating type
# class PostListView(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
    
    
# class PostDetailView(GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     """ getting detail of a post and update or delete that post """    
#     queryset = Post.objects.filter(status=True)
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
    
#     def delete(self, request, *args, **kwargs):
#         self.destroy(request, *args, **kwargs)
        
        
        
# api views
# class PostListView(ListCreateAPIView):
#     """ getting all posts and crating a new post """
#     queryset = Post.objects.filter(status=True)
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializerpermissions
    
    
# class PostDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.filter(status=True)
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer



# view sets
'''
class PostViewSet(viewsets.ViewSet):
    """ craeting a view set for posts to do all request models in one class """
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def list(self, request):
        """ getting all posts """
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    
    
    def create(self, request):
        """ createing a new post """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    def retrieve(self, request, pk=None):
        """ retriving a post """
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)
    
    
    def update(self, request, pk=None):
        """ updating a post """
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
    def destroy(self, request, pk=None):
        """ deleting a post """
        post = get_object_or_404(self.queryset, pk=pk)
        post.delete()
        return Response(
            {
                'detail' : 'object has been deleted'
            }, status=status.HTTP_204_NO_CONTENT
        )'''
        
        
# model view sets
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['title']
    ordering_fields = ['published_time']
    
class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]