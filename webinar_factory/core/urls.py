from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('manage_tags', views.manage_tags, name='manage_tags'),
]
