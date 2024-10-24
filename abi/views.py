from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *

def index(request):

  context = {
    'segment'  : 'index',
  }
  return render(request, "pages/index.html", context)

def teste(request):

  context = {
    'segment'  : 'teste',
  }
  return render(request, "pages/teste.html", context)
