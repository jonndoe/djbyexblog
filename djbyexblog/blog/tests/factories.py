from django.template.defaultfilters import slugify

import factory
import factory.fuzzy

from ..models import Post, Subject
from djbyexblog.users.tests.factories import UserFactory

import pytest

@pytest.fixture
def post():
    return PostFactory()

class SubjectFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))

    class Meta:
        model = Subject


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
    body = factory.Faker('paragraph', nb_sentences=10,)
    #status = factory.fuzzy.FuzzyChoice(
    #    [x[0] for x in Post.STATUS_CHOICES]
    #)
    status = 'published'
    author = factory.SubFactory(UserFactory)
    subject = factory.SubFactory(SubjectFactory)

    class Meta:
        model = Post
