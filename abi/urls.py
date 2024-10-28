from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path('', views.index,  name='index'),
  path('teste/', views.teste,  name='teste'),
  path('cargo/', views.cargo,  name='cargo'),
]