from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Post


class GetPostMixin(object):
    def get_post(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,)
        return post




class PostListView(ListView):
    model = Post
    def get_object(self):
        posts = Post.published.all()
        return posts


class PostDetailView(DetailView):
    model = Post


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request,
                  'blog/post_detail.html',
                  {'post':post})

