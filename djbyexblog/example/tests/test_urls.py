import pytest

from django.urls import reverse, resolve
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db

# this is instead of writing cheese = CheeseFactory()
@pytest.fixture
def cheese():
    return CheeseFactory()


def test_list_reverse():
    # example:list should reverse to /example/
    assert reverse('example:list') == '/example/'

def test_list_resolve():
    # /example/ should resolve to example:list
    assert resolve('/example/').view_name == 'example:list'

def test_add_reverse():
    # example:add should reverse to /example/add/
    assert reverse('example:add') == '/example/add/'

def test_add_resolve():
    # /example/add/ should resolve to 'example:add'
    assert resolve('/example/add/').view_name == 'example:add'

def test_detail_reverse(cheese):
    # example:detail should reverse to /example/cheeseslug/
    url = reverse('example:detail',
                  kwargs={'slug': cheese.slug})
    assert url == f'/example/{cheese.slug}/'

def test_detail_resolve(cheese):
    # /example/cheeseslug/ should resolve to example:detail
    url = f'/example/{cheese.slug}/'
    assert resolve(url).view_name == 'example:detail'


