from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
  password1 = forms.CharField(
      label=_("Senha"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
  )
  password2 = forms.CharField(
      label=_("Confirme a senha"),
      widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a Senha'}),
  )

  class Meta:
    model = User
    fields = ('username', 'email', )

    widgets = {
      'username': forms.TextInput(attrs={
          'class': 'form-control',
          'placeholder': 'Usuário'
      }),
      'email': forms.EmailInput(attrs={
          'class': 'form-control',
          'placeholder': 'E-mail'
      })
    }


class LoginForm(AuthenticationForm):
  username = UsernameField(label=_("Seu Usuário"), widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuário"}))
  password = forms.CharField(
      label=_("Sua Senha"),
      strip=False,
      widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"}),
  )

class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail'
    }))

class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nova Senha'
    }), label="Nova Senha")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirme a nova Senha'
    }), label="Confirme a nova Sinha")
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Senha Antiga'
    }), label='Senha Antiga')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nova Senha'
    }), label="Nova Senha")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirme a nova Senha'
    }), label="Confirme a nova Senha")