from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('manage_tags/', views.manage_tags, name='manage_tags'),
    path('create_webinar/', views.create_webinar, name='create_webinar'),
    path('read_webinar/<int:pk>', views.read_webinar, name='read_webinar'),
    path('update_webinar/<int:pk>', views.update_webinar, name='update_webinar'),
    path('delete_webinar/<int:pk>', views.delete_webinar, name='delete_webinar'),
]
