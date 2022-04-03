import pytest
from django.urls import reverse
from webinar_factory.core.models import Tag
from pytest_django.asserts import assertContains, assertRedirects

# GET
@pytest.fixture
def tags(db):
    return [
        Tag.objects.create(name='Economia'),
        Tag.objects.create(name='Política'),
    ]

# Read
@pytest.fixture
def resposta_get_crud_tags(client, tags):
    return client.get(reverse('core:manage_tags'))

def test_get_crud_tags_status_code(resposta_get_crud_tags):
    assert resposta_get_crud_tags.status_code == 200

def test_crud_tags_form_present(resposta_get_crud_tags):
    assertContains(resposta_get_crud_tags, f'<form action="{reverse("core:manage_tags")}" method="POST"')

def test_btn_submit_present(resposta_get_crud_tags):
    assertContains(resposta_get_crud_tags, '<button type="submit"')

def test_tags_present(resposta_get_crud_tags, tags):
    form_index = 0
    for tag in tags:
        assertContains(
            resposta_get_crud_tags,
            f'<input type="hidden" name="form-{form_index}-id" value="{tag.id}" id="id_form-{form_index}-id">'
        )
        form_index += 1

# POST
@pytest.fixture
def resposta_post_crud_tags(client, tags):
    return client.post(reverse('core:manage_tags'), data={
        'form-TOTAL_FORMS': 3,
        'form-INITIAL_FORMS': 2,
        'form-MIN_NUM_FORMS': 0,
        'form-MAX_NUM_FORMS': 1000,
        # Update
        'form-0-id': 1,
        'form-0-name': 'Economia Austríaca',
        # Delete
        'form-1-id': 2,
        'form-1-name': 'Política',
        'form-1-DELETE': True,
        # Create
        'form-2-id': '',
        'form-2-name': 'Criptomoedas e NFTs',
    })

# For debugging purposes only, do not uncomment
# def test_crud_tags_formset_is_valid(resposta_post_crud_tags):
#     assert not resposta_post_crud_tags.context['formset'].errors

def test_crud_tags_redirection(resposta_post_crud_tags):
    assertRedirects(resposta_post_crud_tags,
                    reverse('core:manage_tags'))

def test_tag_successfully_updated(resposta_post_crud_tags):
    assert Tag.objects.first().name == 'Economia Austríaca'

def test_tag_successfully_deleted(resposta_post_crud_tags):
    assert len(Tag.objects.all()) == 2

def test_tag_successfully_created(resposta_post_crud_tags):
    assert Tag.objects.last().name == 'Criptomoedas e NFTs'