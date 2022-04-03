import pytest
from pytest_django.asserts import assertContains
from django.urls import reverse
from webinar_factory.users.models import User
from webinar_factory.core.models import Webinar, Tag

@pytest.fixture
def tags(db):
    return [
        Tag.objects.create(name='Economia'),
        Tag.objects.create(name='Política'),
    ]

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
def webinar_dashboard_response(client, organizer, webinar):
    client.force_login(organizer)
    return client.get(reverse('core:webinar_dashboard'))

def test_webinar_dashboard_status_code(webinar_dashboard_response):
    assert webinar_dashboard_response.status_code == 200

def test_all_webinars_present(webinar_dashboard_response, organizer):
    webinars = Webinar.objects.filter(organizer=organizer)
    for webinar in webinars:
        assertContains(webinar_dashboard_response, webinar.name)