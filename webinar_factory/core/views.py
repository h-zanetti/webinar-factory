from django.http import Http404
from django.urls import reverse
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
        'title': 'Gerenciar tags',
        'formset': formset
    }

    return render(request, 'core/manage_tags.html', context)

def create_webinar(request):
    if request.method == 'POST':
        form = WebinarCreationForm(request.POST, initial={'organizer': request.user})
        if form.is_valid():
            webinar = form.save()
            messages.success(request, 'Webinário criado com sucesso!')
            return redirect(reverse('core:read_webinar', kwargs={'pk':webinar.pk}))
    else:
        form = WebinarCreationForm(initial={'organizer': request.user})
    
    context = {
        'title': 'Criar novo webinário',
        'form_action': reverse('core:create_webinar'),
        'form': form,
    }
    return render(request, 'core/base_lg_form.html', context)

def read_webinar(request, pk):
    try:
        webinar = Webinar.objects.get(pk=pk)
        context = {
            'title': webinar.name,
            'webinar': webinar,
        }
        return render(request, 'core/read_webinar.html', context)
    except Webinar.DoesNotExist:
        raise Http404('Webinar not found.')