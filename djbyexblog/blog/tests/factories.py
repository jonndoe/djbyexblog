from django.template.defaultfilters import slugify

import factory
import factory.fuzzy

from ..models import Post
from djbyexblog.users.tests.factories import UserFactory

import pytest

@pytest.fixture
def post():
    return PostFactory()


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    body = factory.Faker('paragraph', nb_sentences=6,)
    status = factory.fuzzy.FuzzyChoice(
        [x[0] for x in Post.STATUS_CHOICES]
    )
    author = factory.SubFactory(UserFactory)

    class Meta:
        model = Post
