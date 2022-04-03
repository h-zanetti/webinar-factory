from django.contrib import messages
from django.forms import modelformset_factory
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from webinar_factory.core.models import Tag, Webinar
from webinar_factory.core.forms import TagForm, WebinarCreationForm

def index(request):
    return HttpResponse('Hello, world!')


def manage_tags(request):
    TagFormSet = modelformset_factory(Tag, fields='__all__', can_delete=True, form=TagForm)
    if request.method == 'POST':
        formset = TagFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Tags alteradas com sucesso!')
            return redirect('core:manage_tags')
    else:
        formset = TagFormSet()

    context = {
        'title': 'Gerenciar Tags',
        'formset': formset
    }

    return render(request, 'core/manage_tags.html', context)
