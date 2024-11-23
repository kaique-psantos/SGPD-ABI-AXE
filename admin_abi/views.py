from django.shortcuts import render, redirect
from admin_abi.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from .forms import FormularioUpdateUser
from django.contrib import messages

def index(request):
  context = {
    'segment': 'index'
  }
  return render(request, "pages/index.html", context)

# Authentication
class UserRegistrationView(CreateView):
  template_name = 'accounts/auth-signup.html'
  form_class = RegistrationForm
  success_url = '/accounts/login/'

class UserLoginView(LoginView):
  template_name = 'accounts/auth-signin.html'
  form_class = LoginForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/auth-reset-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/auth-password-reset-confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/auth-change-password.html'
  form_class = UserPasswordChangeForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

@login_required(login_url='/accounts/login/')
def profile(request):
  user = request.user
  context = {
    'segment': 'profile',
    'nome': user.first_name,
    'sobrenome': user.last_name,
    'email': user.email,
    'usuario': user.username,
  }
  return render(request, 'pages/profile.html', context)

@login_required(login_url='/accounts/login/')
def profile_update(request):

  if request.method == 'POST':
    form = FormularioUpdateUser(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Seu perfil foi atualizado com sucesso!')
      return redirect('profile')
  else:
    form = FormularioUpdateUser(instance=request.user)

  context = {
    'form': form,
  }
  return render(request, 'pages/profile_update.html', context)


