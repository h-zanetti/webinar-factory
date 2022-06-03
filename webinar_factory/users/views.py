from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from webinar_factory.users.forms import UserCreationForm, UserUpdateForm

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
        'title': 'Boas-vindas!',
        'form_action': reverse('register'),
        'form': form,
    }
    return render(request, 'users/register.html', context)

@login_required(login_url='/users/login/')
def update_user(request):
    user = request.user
    if not user.is_authenticated:
        return Http404()    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil alterado com sucesso!')
            return redirect('update_user')
    else:
        form = UserUpdateForm(instance=user)

    context = {
        'title': 'Atualizar usuário',
        'form_action': reverse('update_user'),
        'user': user,
        'form': form,
    }
    return render(request, 'core/login.html', context)
