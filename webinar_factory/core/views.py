from django.shortcuts import render
from  django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required(login_url='/login/')
def index(request):
    return render(request, 'core/index.html')
