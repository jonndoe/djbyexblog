import pytest
from pytest_django.asserts import assertContains, assertRedirects

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware

from django.test import RequestFactory

from djbyexblog.users.models import User
from ..models import Post
from ..views import (
           #PostCreateView,
           PostListView,
           PostDetailView,
           post_detail,
)
from .factories import PostFactory, post

pytestmark = pytest.mark.django_db

# rf is a fixture, user_admin is a fixture.


def test_post_list_view(rf):
    request = rf.get(reverse('blog:list'))
    response = PostListView.as_view()(request)
    assertContains(response, 'Post List')

def test_post_detail_cbv_view(rf,post, admin_user):

    url = reverse('blog:detail',
                  args=[post.publish.year,
                        post.publish.month,
                        post.publish.day,
                        post.slug,])

    print(url, '************************************************')
    print(post.slug, "slugslugslug******************************************************")
    request = rf.get(url)
    print(request, '***********************************************')

    callable_obj = PostDetailView.as_view()

    print(callable_obj, '************************************************')
    response = callable_obj(request, year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post.slug)

    print(response, '*******************************************************')
    assertContains(response, post.title)


def test_post_detail_fbv_view(rf, post):
    url = reverse('blog:detail',
                  args=[post.publish.year,
                        post.publish.month,
                        post.publish.day,
                        post.slug,])

    print(url, '************************************************')
    print(post.slug, "slugslugslug******************************************************")
    request = rf.get(url)
    print(request, '***********************************************')

    callable_obj = post_detail

    print(callable_obj, '************************************************')
    response = callable_obj(request, year=post.publish.year, month=post.publish.month, day=post.publish.day, slug=post)

    print(response, '*******************************************************')
    assertContains(response, post.title)
