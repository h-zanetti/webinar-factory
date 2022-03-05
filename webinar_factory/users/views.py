from django.http import Http404
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from webinar_factory.users.forms import UserCreationForm, UserEditForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:index')
    else:
        form = UserCreationForm()
    
    context = {
        'title': 'Registration',
        'form': form,
    }
    return render(request, 'users/register.html', context)

def perfil(request):
    user = request.user
    if not user.is_authenticated:
        return Http404()    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil alterado com sucesso!')
            return redirect('perfil')
    else:
        form = UserEditForm(instance=user)

    context = {
        'user': user,
        'form': form,
    }
    return render(request, 'users/perfil.html', context)
