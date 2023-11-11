from django.urls import path, include
from blog.api.v1.views import *
from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register('post', PostViewSet, basename='post')

router = DefaultRouter()
router.register("post", PostModelViewSet, basename="post")
router.register("category", CategoryModelViewSet, basename="category")

app_name = "blog-api-v1"

urlpatterns = [
    # path('posts/', post_list_view, name='post-list'),
    # path('posts/', PostListView.as_view(), name='post-list'),
    # path('posts/<int:pk>/', post_detail_view , name='post-detail'),
    # path('posts/<int:pk>/', PostDetailView.as_view() , name='post-detail'),
    # path('posts/', PostViewSet.as_view(
    #     {
    #         'get' : 'list',
    #         'post' : 'create'
    #     }
    #     ), name='post-viewset'),
    # path('posts/<int:pk>/', PostViewSet.as_view(
    #     {
    #         'get' : 'retrieve',
    #         'put' : 'update',
    #         'delete' : 'destroy'
    #     }
    #     ), name='post-viewset'),
    path("", include(router.urls), name="blog-router")
]
