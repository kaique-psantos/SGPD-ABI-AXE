from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from  abi.models import Pessoa, Genero, OrientacaoSexual, Etnia, Escolaridade, AreaArtistica



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
    
class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['pes_nome', 'pes_data_nascimento', 'pes_cpf', 'gen_cod', 'ori_cod', 'etn_cod', 'esc_cod', 'are_cod', 'pes_email', 'pes_celular', 'pes_data_ingresso']

    # Validação personalizada de campos
    def clean_pes_nome(self):
        nome = self.cleaned_data.get('pes_nome')
        if not nome:
            raise forms.ValidationError("O campo Nome é obrigatório.")
        return nome

    def clean_pes_cpf(self):
        cpf = self.cleaned_data.get('pes_cpf')
        if not cpf:
            raise forms.ValidationError("O campo CPF é obrigatório.")
        # validação do CPF
        return cpf

    def clean_pes_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('pes_data_nascimento')
        if not data_nascimento:
            raise forms.ValidationError("O campo Data de Nascimento é obrigatório.")
        return data_nascimento
    
    def clean_pes_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('pes_data_nascimento')
        if not data_nascimento:
            raise forms.ValidationError("O campo Data de Nascimento é obrigatório.")
        return data_nascimento
    
    def clean_pes_email(self):
            pes_email = self.cleaned_data.get('pes_email')
            if not pes_email:
                raise forms.ValidationError("O campo E-mail é obrigatório.")
            return pes_email
        
    def clean_pes_data_ingresso(self):
            pes_data_ingresso = self.cleaned_data.get('pes_data_ingresso')
            if not pes_data_ingresso:
                raise forms.ValidationError("O campo Data de Cadastro é obrigatório.")
            return pes_data_ingresso
        
    def clean_gen_cod(self):
        genero = self.cleaned_data.get('gen_cod')
        if not genero:
            raise forms.ValidationError("O campo Gênero é obrigatório.")
        return genero
