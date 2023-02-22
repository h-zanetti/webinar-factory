from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models.functions import Concat
from django.forms import modelformset_factory
from django.db.models import CharField, Value
from django.contrib.auth.decorators import login_required

from webinar_factory.core.models import Tag, Webinar
from webinar_factory.core.forms import TagForm, WebinarForm, WebinarFilters


@login_required(login_url='/users/login/')
def index(request):
    return render(request, 'core/index.html')

@login_required(login_url='/users/login/')
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

@login_required(login_url='/users/login/')
def create_webinar(request):
    if request.method == 'POST':
        form = WebinarForm(request.POST, initial={'organizer': request.user})
        if form.is_valid():
            webinar = form.save()
            messages.success(request, 'Webinário criado com sucesso!')
            return redirect(reverse('core:read_webinar', kwargs={'pk':webinar.pk}))
    else:
        form = WebinarForm(initial={'organizer': request.user})
    
    context = {
        'title': 'Criar novo webinário',
        'form_action': reverse('core:create_webinar'),
        'form': form,
    }
    return render(request, 'core/base_lg_form.html', context)

@login_required(login_url='/users/login/')
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

@login_required(login_url='/users/login/')
def update_webinar(request, pk):
    try:
        webinar = Webinar.objects.get(pk=pk)
        if request.method == 'POST':
            form = WebinarForm(request.POST, instance=webinar)
            if form.is_valid():
                webinar = form.save()
                messages.success(request, 'Webinário atualizado com sucesso.')
                return redirect(reverse('core:read_webinar', kwargs={'pk':webinar.pk}))
        else:
            form = WebinarForm(instance=webinar)
        
        context = {
            'title': 'Atualizar webinário',
            'webinar': webinar,
            'form': form,
            'form_action': reverse('core:update_webinar', kwargs={'pk': pk}),
        }
        return render(request, 'core/base_lg_form.html', context)
    except Webinar.DoesNotExist:
        raise Http404('Webinar not found.')

@login_required(login_url='/users/login/')
def delete_webinar(request, pk):
    try:
        webinar = Webinar.objects.get(pk=pk)
        if request.method == 'POST':
            webinar.delete()
            # TODO: redirect to dashboard
            return redirect('core:index')
    except Webinar.DoesNotExist:
        raise Http404('Webinar not found.')

def webinar_dashboard(request):
    context = {
        'title': 'Dashboard',
        'user': request.user,
        'webinars': Webinar.objects.filter(organizer=request.user)
    }
    return render(request, 'core/dashboard.html', context)

def webinar_list(request):
    if request.GET:
        form = WebinarFilters(request.GET)
        if form.is_valid():
            query_dict = dict()
            name = form.cleaned_data.get('name')
            if name:
                query_dict['name__contains'] = name
            tags = form.cleaned_data.get('tags')
            if tags:
                query_dict['tags__in'] = tags
            speaker = form.cleaned_data.get('speaker')
            if speaker:
                query_dict['full_names__icontains'] = speaker
            start_dt = form.cleaned_data.get('start_dt')
            if start_dt:
                query_dict['start_dt__gte'] = start_dt
            end_dt = form.cleaned_data.get('end_dt')
            if end_dt:
                query_dict['end_dt__lte'] = end_dt
            ticket_price_min = form.cleaned_data.get('price_min')
            if type(ticket_price_min) == float:
                query_dict['ticket_price__gte'] = ticket_price_min
            ticket_price_max = form.cleaned_data.get('price_max')
            if type(ticket_price_max) == float:
                query_dict['ticket_price__lte'] = ticket_price_max

            queryset = Webinar.objects.annotate(full_names=Concat('speakers__first_name', Value(' '), 'speakers__last_name'))
            queryset = queryset.filter(**query_dict)
    else:
        form = WebinarFilters()
        queryset = Webinar.objects.all()

    context = {
        'form': form,
        'webinars': queryset
    }
    return render(request, 'core/webinar_list.html', context)