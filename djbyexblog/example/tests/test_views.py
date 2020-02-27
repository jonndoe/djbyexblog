import pytest
from pytest_django.asserts import assertContains, assertRedirects

from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware

from django.test import RequestFactory

from djbyexblog.users.models import User
from ..models import Cheese
from ..views import (
           CheeseCreateView,
           CheeseListView,
           CheeseDetailView,
)
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db

# rf is a fixture, user_admin is a fixture.


def test_good_cheese_list_view(rf):
    request = rf.get(reverse('example:list'))
    response = CheeseListView.as_view()(request)
    assertContains(response, 'Cheese List')

def test_good_cheese_detail_view(rf, admin_user):
    cheese = CheeseFactory()
    url = reverse('example:detail',
                  kwargs={'slug': cheese.slug})
    request = rf.get(url)
    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)

def test_good_cheese_create_view(rf, admin_user):

    cheese = CheeseFactory()

    request = rf.get(reverse("example:add"))


    # we need authenticated user
    request.user = admin_user

    response = CheeseCreateView.as_view()(request)

    assert response.status_code == 200
    assert cheese.creator == User.objects.get(username=cheese.creator)


def test_list_cheese_contains_2_cheeses(rf):
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()

    request = rf.get(reverse('example:list'))
    response = CheeseListView.as_view()(request)

    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_detail_contains_cheese_data(rf):
    cheese = CheeseFactory()

    url = reverse("example:detail",
                  kwargs={'slug': cheese.slug})
    request = rf.get(url)

    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)

    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_cheese_create_form_valid(rf, admin_user):
    # Submit the cheese add form
    form_data = {
        "name": "Paski Sir",
        "description": "A salty hard cheese",
        "firmness": Cheese.Firmness.HARD,
    }

    request = rf.post(reverse("example:add"), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    cheese = Cheese.objects.get(name="Paski Sir")

    assert cheese.description == "A salty hard cheese"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user
