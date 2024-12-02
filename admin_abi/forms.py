from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from abi.models import *
from django.forms.models import inlineformset_factory


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

class FormularioUpdateUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

        labels = {
            'username': 'Usuário',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class FormularioUpdatePessoa(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['pes_nome', 'pes_cpf', 'pes_email']
        widgets = {
            'pes_nome': forms.TextInput(attrs={'class': 'form-control'}),
            'pes_cpf': forms.DateInput(attrs={'class': 'form-control'}),
            'pes_email': forms.DateInput(attrs={'class': 'form-control'}),
        }

class FormularioCriarUser(UserCreationForm):
    pessoa = forms.ModelChoiceField(
        queryset=Pessoa.objects.all(),
        required=False,
        label="Pessoa",
        help_text="Selecione uma Pessoa existente para vincular a este usuário."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Campos padrão

    def save(self, commit=True):
        user = super().save()
        pessoa = self.cleaned_data.get('pessoa')

        UsuarioPessoa.objects.create(user=user, pes_cod=pessoa)

        if not pessoa:
            user.first_name = user.username
            user.save()
        else:
            user.first_name = pessoa.pes_nome
            user.save()

        return user