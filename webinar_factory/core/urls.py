from django.urls import path, include
from .views import index
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
