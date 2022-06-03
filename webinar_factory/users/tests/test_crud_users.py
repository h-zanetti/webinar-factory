import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse
from webinar_factory.users.models import User

# Create
# GET
# @pytest.fixture
# def resposta_register_get(client, db):
#     return client.get(reverse('register'))

# def test_register_status_code(resposta_register_get):
#     assert resposta_register_get.status_code == 200

# def test_form_present(resposta_register_get):
#     assertContains(resposta_register_get, f'<form action="{reverse("register")}" method="POST"')

# def test_btn_submit_present(resposta_register_get):
#     assertContains(resposta_register_get, '<button type="submit"')

# # POST
# @pytest.fixture
# def resposta_register_post(client, db):
#     return client.post(reverse('register'), data={
#         'email': 'root@liberaction.com.br',
#         'first_name': 'Root',
#         'last_name': 'User',
#         'password1': 'testingUser123',
#         'password2': 'testingUser123',
#     })

# # def test_sem_erros(resposta_register_post):
# #     assert not resposta_register_post.context['form'].errors

# def test_register_redirection(resposta_register_post):
#     # TODO: Redirects to profile
#     assertRedirects(resposta_register_post, reverse('core:index'))

# def test_user_exists(resposta_register_post):
#     assert User.objects.exists()

# def test_user_autenticated(resposta_register_post):
#     assert resposta_register_post.wsgi_request.user.is_authenticated

# Read
# GET
# POST

# Update
# GET
@pytest.fixture
def user(db):
    return User.objects.create_user(email='root@liberaction.com.br', password='testingUser123')

@pytest.fixture
def resposta_get_update_user(client, user):
    client.force_login(user)
    return client.get(reverse('update_user'))

def test_get_update_user_status_code(resposta_get_update_user):
    assert resposta_get_update_user.status_code == 200

def test_form_present(resposta_get_update_user):
    assertContains(
        resposta_get_update_user, 
        f'<form action="{reverse("update_user")}" method="POST"')

# POST
@pytest.fixture
def resposta_post_update_user(client, user):
    client.force_login(user)
    return client.post(reverse('update_user'), data={
        'email': 'root@liberaction.com.br',
        'first_name': 'Root',
        'last_name': 'User',
    })

def test_post_update_user_redirection(resposta_post_update_user):
    assertRedirects(resposta_post_update_user, reverse('update_user'))

def test_update_user_changed(resposta_post_update_user):
    assert User.objects.first().first_name == 'Root'

# Delete
# GET
# POST
