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
                    reverse('core:read_webinar', kwargs={'pk': 1}))

def test_webinar_successfully_created(response_post_create_webinar):
    assert Webinar.objects.exists()

def test_organizer_is_webinar_creator(response_post_create_webinar):
    webinar = Webinar.objects.first()
    organizer = User.objects.get(email='organizer@webinarfactory.com.br')
    assert webinar.organizer == organizer

# Read 
@pytest.fixture
def webinar(organizer, speaker, tags):
    instance =  Webinar.objects.create(
        name='Blockchain 101: Criptomoedas e NFTs',
        organizer=organizer,
        description='Cool stuff!',
        ticket_price=100,
        start_dt='2020-04-01 09:00:00',
        end_dt='2020-04-01 14:00:00',
    )
    instance.speakers.add(speaker)
    for tag in tags:
        instance.tags.add(tag.id)
    return instance

@pytest.fixture
def response_get_read_webinar(client, webinar):
    return client.get(reverse(
        'core:read_webinar', kwargs={'pk':webinar.pk}))

def test_read_webinar_status_code(response_get_read_webinar):
    assert response_get_read_webinar.status_code == 200

def test_webinar_present(response_get_read_webinar, webinar):
    assertContains(response_get_read_webinar, webinar.name)
    assertContains(response_get_read_webinar, webinar.organizer.get_full_name())
    assertContains(response_get_read_webinar, webinar.description)
    assertContains(response_get_read_webinar, webinar.ticket_price)

def test_speakers_present_read_webinar(response_get_read_webinar, webinar):
    for speaker in webinar.speakers.all():
        assertContains(response_get_read_webinar, speaker.get_full_name())

def test_tags_present_read_webinar(response_get_read_webinar, webinar):
    for tag in webinar.tags.all():
        assertContains(response_get_read_webinar, tag.name)


# Update

# GET
@pytest.fixture
def response_get_update_webinar(client, webinar):
    return client.get(reverse(
        'core:update_webinar', kwargs={'pk':webinar.pk}))

def test_update_webinar_status_code(response_get_update_webinar):
    assert response_get_update_webinar.status_code == 200

def test_update_webinar_form_present(response_get_update_webinar, webinar):
    assertContains(
        response_get_update_webinar,
        f'<form action="{reverse("core:update_webinar", kwargs={"pk":webinar.pk})}" method="POST"')

def test_update_webinar_submit_btn_present(response_get_update_webinar):
    assertContains(response_get_update_webinar, '<button type="submit"')

# POST
@pytest.fixture
def response_post_update_webinar(client, webinar, speaker, tags):
    return client.post(reverse(
        'core:update_webinar', kwargs={'pk':webinar.pk}),
        data={
            'name': 'Economia Austríaca',
            'speakers': [speaker.id],
            'tags': [tag.id for tag in tags],
            'description': 'Cool stuff!',
            'ticket_price': 100,
            'start_dt': '2020-04-01 09:00:00',
            'end_dt': '2020-04-01 14:00:00',
        })

def test_update_webinar_redirection(response_post_update_webinar):
    assertRedirects(response_post_update_webinar,
                    reverse('core:read_webinar', kwargs={'pk': 1}))

def test_webinar_successfully_updated(response_post_update_webinar):
    assert Webinar.objects.first().name == 'Economia Austríaca'


# Delete

# GET
# POST
