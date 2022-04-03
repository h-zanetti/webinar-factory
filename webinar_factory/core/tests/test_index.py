import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def index_unathenticated_response(client):
    response = client.get(reverse('core:index'))
    return response

def test_index_redirection(index_unathenticated_response):
    assert index_unathenticated_response.status_code == 302

@pytest.fixture
def index_response(client, db):
    user = User.objects.create_user(username='root', password='testingUser123')
    client.force_login(user)
    response = client.get(reverse('core:index'))
    return response

def test_index_status_code(index_response):
    assert index_response.status_code == 200

