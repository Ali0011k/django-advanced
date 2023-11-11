from django.urls import path, include
from blog.views import *

app_name = "blog"

urlpatterns = [
    path("", IndexView.as_view(), name="cbv-index"),
    path("redirect/", RedirectViewCbv.as_view(), name="redirect-cbv"),
    path(
        "redirect-to-index/",
        RedirectToIndexView.as_view(),
        name="redirect_to_index-cbv",
    ),
    path("posts/cbv/", PostList.as_view(), name="PostList-cbv"),
    path("posts/fbv/", postlist, name="PostList-fbv"),
    path("posts/cbv/<int:pk>/", PostDetail.as_view(), name="post-detail"),
    # path('posts/create/', CreatePost.as_view(), name='create-post'),
    path("posts/create/", CreatePostView.as_view(), name="create-post"),
    path("posts/cbv/<int:pk>/update/", UpdatePostView.as_view(), name="update-post"),
    path("posts/cbv/<int:pk>/delete/", DeletePostView.as_view(), name="delete-post"),
    path("api/v1/", include("blog.api.v1.urls")),
]
