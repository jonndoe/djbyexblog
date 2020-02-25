import pytest

pytestmark = pytest.mark.django_db


from ..models import Cheese
from .factories import CheeseFactory


def test___str__():
    cheese = CheeseFactory()
    assert cheese.__str__() == cheese.name

def test_get_absolute_url():
    cheese = CheeseFactory()
    url = cheese.get_absolute_url()
    assert url == f'/example/{cheese.slug}/'
