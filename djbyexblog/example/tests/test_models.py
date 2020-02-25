import pytest

pytestmark = pytest.mark.django_db


from ..models import Cheese


def test___str__():
    cheese = Cheese.objects.create(
        name="Stracchino",
        description="Semi-sweet cheese",
        firmness=Cheese.Firmness.SOFT,
    )
    assert cheese.__str__() == "Stracchino"
