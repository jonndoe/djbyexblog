import pytest

pytestmark = pytest.mark.django_db

from ..models import Post
from .factories import PostFactory


def test___str__():
    post = PostFactory()
    assert post.__str__() == post.title

def test_get_absolute_url():
    post = PostFactory()
    url = post.get_absolute_url()
    assert url == f'/blog/{post.publish.year}/{post.publish.month}/{post.publish.day}/{post.slug}/'
