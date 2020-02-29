from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    View,
    TemplateView,
)
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from .models import Post, Subject
from django.db.models import Count
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class GetPostMixin(object):
    def get_post(self, request, year, month, day, post):
        post = get_object_or_404(Post, slug=post,
                                 status='published',
                                 publish__year=year,
                                 publish__month=month,
                                 publish__day=day,)
        return post




class PostListView(TemplateResponseMixin, View):
    model = Post
    template_name = 'blog/post_list.html'
    def get_object(self):
        posts = Post.published.all()
        return posts

    def get(self, request, subject=None, tag_slug=None):
        subjects = Subject.objects.annotate(
            total_posts=Count('posts'))
        posts = Post.published.annotate(
            total_contents=Count('contents'))
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            posts = posts.filter(subject=subject)
        tag = None
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
            print(posts)
            tagged_posts = len(posts)
        else:
            tagged_posts = None

        #pagination
        paginator = Paginator(posts, 3) # 3 posts in each page
        page = request.GET.get('page')
        tags = Tag.objects.all()
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # if page is not an iteger deliver the first page
            posts = paginator.page(1)
        except EmptyPage:
            # if page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)

        return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'page': page,
                                        'posts': posts,
                                        'tagged_posts': tagged_posts,
                                        'tag': tag,
                                        'tags': tags,
                                        'section': 'posts'})




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

