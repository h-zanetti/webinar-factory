import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def index_response(client):
    response = client.get(reverse('core:index'))
    return response

def test_index_status_code(index_response):
    assert index_response.status_code == 200
