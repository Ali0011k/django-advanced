from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import *
from blog.forms import *
from blog.models import *


# class based views
class IndexView(TemplateView):
    template_name = "index.html"
    extra_context = {"name": "ali"}


class RedirectViewCbv(RedirectView):
    url = "https://google.com"


class RedirectToIndexView(RedirectView):
    pattern_name = "blog:cbv-index"


class PostList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    # model = Post
    permission_required = "blog.view_post"
    queryset = Post.objects.filter(status=True)
    paginate_by = 2
    ordering = "-id"
    context_object_name = "posts"
    template_name = "blog/postlist.html"


class PostDetail(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Post
    permission_required = "blog.view_post"
    context_object_name = "post"
    template_name = "blog/postdetail.html"
    pk_url_kwarg = "pk"


class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    template_name = "blog/create_post.html"
    form_class = CreatePostForm
    success_url = "/blog/posts/cbv/"
    permission_required = "blog.add_post"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CreatePostView(CreateView):
    model = Post
    template_name = "blog/post_create.html"
    fields = ["category", "title", "content", "status", "published_time"]
    success_url = "/blog/posts/cbv/"

    def form_valid(self, form):
        form.instance.author = User.objects.get(email="kly441781@gmail.com")
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/update_post.html"
    fields = ["category", "title", "content", "status", "published_time"]
    permission_required = "blog.change_post"

    def get_success_url(self):
        url = self.request.path.replace("/update/", "")
        return f"{url}"


class DeletePostView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/posts/cbv/"
    template_name = "blog/post_confirm_delete.html"
    permission_required = "blog.delete_post"


def postlist(request):
    posts = Post.objects.all().order_by("-id")
    # create a pageinator and return it in template
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # render pagination with posts objects in pageination
    return render(
        request,
        "blog/postlist.html",
        {
            "page_obj": page_obj,
        },
    )
