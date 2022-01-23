from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            auth_user = authenticate(username=username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('core:index')
    else:
        form = UserCreationForm()

    context = {
        'title': 'Sign Up',
        'form': form
    }
    return render(request, 'core/register.html', context)

def index(request):
    return render(request, 'core/index.html')
