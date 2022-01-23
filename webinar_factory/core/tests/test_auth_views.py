import pytest
from django.contrib.auth.models import User
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse

# GET login
@pytest.fixture
def resposta_login_get(client, db):
    return client.get(reverse('core:login'))

def test_login_status_code(resposta_login_get):
    assert resposta_login_get.status_code == 200

def test_form_present(resposta_login_get):
    assertContains(resposta_login_get, f'<form action="{reverse("core:login")}" method="POST"')

def test_btn_submit_present(resposta_login_get):
    assertContains(resposta_login_get, '<button type="submit"')

# POST login
@pytest.fixture
def resposta_login_post(client, db):
    User.objects.create_user(username='root', password='testingUser123')
    return client.post(reverse('core:login'), data={
        'username': 'root',
        'password': 'testingUser123',
    })

def test_user_autenticated(resposta_login_post):
    assert resposta_login_post.wsgi_request.user.is_authenticated == True

def test_login_post_redirection(resposta_login_post):
    assertRedirects(resposta_login_post, reverse('core:index'))

# logout
@pytest.fixture
def user(db):
    return User.objects.create_user(username='root', password='testingUser123')

@pytest.fixture
def resposta_logout(client, user):
    client.force_login(user)
    return client.get(reverse('core:logout'))

def test_user_not_autenticated(resposta_logout):
    assert not resposta_logout.wsgi_request.user.is_authenticated

# Register
@pytest.fixture
def resposta_register(client, db):
    return client.post(reverse('core:register'), data={
        'username': 'root',
        'password1': 'testingUser123',
        'password2': 'testingUser123',
    })

# def test_registration_form_is_valid(resposta_register):
#     assert not resposta_register.context['form'].errors

def test_register_post_redirection(resposta_register):
    assertRedirects(resposta_register, reverse('core:index'))

def test_user_exists(resposta_register):
    assert User.objects.exists()

def test_registered_user_authenticated(resposta_register):
    assert resposta_register.wsgi_request.user.is_authenticated == True
