import pytest
from django.urls import reverse
from webinar_factory.users.models import User

@pytest.fixture
def index_unathenticated_response(client):
    response = client.get(reverse('core:index'))
    return response

def test_index_redirection(index_unathenticated_response):
    assert index_unathenticated_response.status_code == 302

@pytest.fixture
def user(db):
    return User.objects.create_user(email='root@webinarfactory.com.br', password='ineditaPamonha')

@pytest.fixture
def index_response(client, user):
    client.force_login(user)
    response = client.get(reverse('core:index'))
    return response

def test_index_status_code(index_response):
    assert index_response.status_code == 200

