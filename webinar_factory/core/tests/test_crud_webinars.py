import pytest
from django.urls import reverse
from webinar_factory.core.models import Tag, Webinar
from webinar_factory.users.models import User
from pytest_django.asserts import assertContains, assertRedirects

@pytest.fixture
def tags(db):
    return [
        Tag.objects.create(name='Economia'),
        Tag.objects.create(name='Política'),
    ]

# Create Webinar

# GET
@pytest.fixture
def response_get_create_webinar(client, tags):
    return client.get(reverse('core:create_webinar'))

def test_create_webinar_status_code(response_get_create_webinar):
    assert response_get_create_webinar.status_code == 200

def test_create_webinar_form_present(response_get_create_webinar):
    assertContains(response_get_create_webinar, f'<form action="{reverse("core:create_webinar")}" method="POST"')

def test_create_webinar_submit_btn_present(response_get_create_webinar):
    assertContains(response_get_create_webinar, '<button type="submit"')

# POST
@pytest.fixture
def organizer(db):
    return User.objects.create(
        email='organizer@webinarfactory.com.br',
        password='testingUser123',
        is_organizer=True
    )

@pytest.fixture
def speaker(db):
    return User.objects.create(
        email='speaker@webinarfactory.com.br',
        password='testingUser123',
        is_speaker=True
    )

@pytest.fixture
def response_post_create_webinar(client, tags, organizer, speaker):
    client.force_login(organizer)
    return client.post(reverse('core:create_webinar'), data={
        'name': 'Blockchain 101: Criptomoedas e NFTs',
        'speakers': [speaker.id],
        'tags': [tag.id for tag in tags],
        'description': 'Cool stuff!',
        'ticket_price': 100,
        'start_dt': '2020-04-01 09:00:00',
        'end_dt': '2020-04-01 14:00:00',
    })

def test_create_webinar_redirection(response_post_create_webinar):
    assertRedirects(response_post_create_webinar,
                    reverse('core:index'))

def test_webinar_successfully_created(response_post_create_webinar):
    assert Webinar.objects.exists()

def test_organizer_is_webinar_creator(response_post_create_webinar):
    webinar = Webinar.objects.first()
    organizer = User.objects.get(email='organizer@webinarfactory.com.br')
    assert webinar.organizer == organizer
