from django.shortcuts import render, redirect, get_object_or_404
from abi.models import Pessoa, UsuarioPessoa, MembroDiretoria, Cargo
from admin_abi.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, \
  UserSetPasswordForm, FormularioUpdateUser, FormularioUpdatePessoa
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from datetime import date

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
  pessoa_existe = UsuarioPessoa.objects.filter(user=user).exists()
  if pessoa_existe:
    pessoa = UsuarioPessoa.objects.get(user=user)
    cargo = MembroDiretoria.objects.get(pes_cod=pessoa.pes_cod)

    data=pessoa.pes_cod.pes_data_ingresso
    formato = date(data.year, data.month, data.day)
    data_formatada = formato.strftime("%d/%m/%Y")

    context = {
      'segment': 'profile',
      'nome': pessoa.pes_cod.pes_nome,
      'sobrenome': user.last_name,
      'email': user.email,
      'usuario': user.username,
      'cargo': f'Cargo: {cargo.car_cod} - {pessoa.pes_cod.are_cod}',
      'dt_ingresso': f'Data de Ingresso: {data_formatada}',
      'existe': pessoa_existe,
    }
  else:
    context = {
      'segment': 'profile',
      'usuario': user.username,
      'existe': pessoa_existe,
    }

  return render(request, 'pages/profile.html', context)

@login_required(login_url='/accounts/login/')
def profile_update(request):
  user = request.user
  pessoa_existe = UsuarioPessoa.objects.filter(user=user).exists()
  if pessoa_existe:
    pessoa = UsuarioPessoa.objects.get(user=user)
    cargo = MembroDiretoria.objects.get(pes_cod=pessoa.pes_cod)

    data = pessoa.pes_cod.pes_data_ingresso
    formato = date(data.year, data.month, data.day)
    data_formatada = formato.strftime("%d/%m/%Y")

    if request.method == 'POST':
      formPessoa = FormularioUpdatePessoa(request.POST, instance=pessoa.pes_cod)
      formUser = FormularioUpdateUser(request.POST, instance=request.user)
      if formPessoa.is_valid() and formUser.is_valid():
        formPessoa.save()
        formUser.save()
        return redirect('profile')
    else:
      formPessoa = FormularioUpdatePessoa(instance=pessoa.pes_cod)
      formUser = FormularioUpdateUser(instance=request.user)

    context = {
        'formPessoa': formPessoa,
        'formUser': formUser,
        'user': user,
        'nome': pessoa.pes_cod.pes_nome,
        'email': pessoa.pes_cod.pes_email,
        'cargo': f'Cargo: {cargo.car_cod} - {pessoa.pes_cod.are_cod}',
        'dt_ingresso': f'Data de Ingresso: {data_formatada}',
        'existe': pessoa_existe,
      }
  else:
    if request.method == 'POST':
      formUser = FormularioUpdateUser(request.POST, instance=request.user)
      if formUser.is_valid():
        formUser.save()
        return redirect('profile')
    else:
      formUser = FormularioUpdateUser(instance=request.user)

    context = {
      'formUser': formUser,
      'usuario': user.username,
      'existe': pessoa_existe,
    }

  return render(request, 'pages/profile_update.html', context)
