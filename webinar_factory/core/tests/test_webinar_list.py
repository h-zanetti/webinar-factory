import pytest
from django.urls import reverse
from webinar_factory.core.models import Webinar, Tag
from webinar_factory.users.models import User


@pytest.fixture
def webinars(db):
    tags = [Tag.objects.create(name='Economia'),
            Tag.objects.create(name='Política')]
    organizer = User.objects.create(email='organizer@webinarfactory.com.br',
                                    password='testingUser123',
                                    is_organizer=True)
    speaker = User.objects.create(email='speaker@webinarfactory.com.br',
                                  password='testingUser123',
                                  is_speaker=True)
    wlist = []
    wnames = ['Blockchain 101: Criptomoedas e NFTs',
              'Ética da Liberdade']
    for n, t in zip(wnames, tags):
        webinar = Webinar.objects.create(name=n,
                                         organizer=organizer,
                                         description='Cool stuff!',
                                         ticket_price=100,
                                         start_dt='2020-04-01 09:00:00',
                                         end_dt='2020-04-01 14:00:00')
        webinar.tags.add(t)
        webinar.speakers.add(speaker)
        wlist.append(webinar)
    return wlist

def test_filter_webinar_by_name(client, webinars):
    response = client.get(reverse('core:webinar_list'), data={'name': 'blockchain'})
    assert response.status_code == 200
    assert len(response.context['webinars']) == 1
    assert response.context['webinars'][0].name == 'Blockchain 101: Criptomoedas e NFTs'


def test_filter_webinar_by_tag(client, webinars):
    response = client.get(reverse('core:webinar_list'), data={'tags': [2]})
    assert response.status_code == 200
    assert len(response.context['webinars']) == 1
    assert response.context['webinars'][0].name == 'Ética da Liberdade'

def test_filter_webinar_by_speaker(client, webinars):
    response = client.get(reverse('core:webinar_list'), data={'speakers': [1]})
    assert response.status_code == 200
    assert len(response.context['webinars']) == 2

def test_filter_webinar_all(client, webinars):
    response = client.get(reverse('core:webinar_list'), data={'name': 'English'})
    assert response.status_code == 200
    assert len(response.context['webinars']) == 0
