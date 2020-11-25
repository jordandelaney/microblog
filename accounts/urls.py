"""Defines URL patterns for users"""

from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    #include default auth urls
    path('', include('django.contrib.auth.urls')),
    #registration page
    path('register/', views.register, name='register'),
    # User profile page
    path('my-profile/', views.profile, name='profile'),
]