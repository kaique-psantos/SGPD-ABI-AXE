from django.urls import path
from django.contrib.auth import views as auth_views
from .views import pessoa_view
from . import views

urlpatterns = [
  path('', views.dashboard,  name='index'),
  path('dashboard/', views.dashboard, name='dashboard'),
  path('imprimir/oficio/<int:ofi_cod>/', views.imprimir_oficio, name='oficio_imprimir'),
]

