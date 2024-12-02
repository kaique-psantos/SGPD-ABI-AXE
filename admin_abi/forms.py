from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from abi.models import *
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError

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

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("Este nome de usuário já está em uso. Por favor, escolha outro.")

        return username

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['pes_nome', 'pes_data_nascimento', 'pes_cpf', 'pes_email', 'pes_telefone',
                'pes_celular', 'cid_naturalidade', 'est_naturalidade', 'end_cod', 
                'ori_cod', 'gen_cod', 'esc_cod', 'etn_cod', 'pes_data_ingresso', 
                'pes_data_saida', 'pes_ativo', 'are_cod', 'pes_imagem', 'cid_cod', 
                'est_cod', 'end_rua', 'end_bairro', 'end_numero', 'end_complemento', 
                'end_referencia']

    
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

        if not pessoa:
            user.first_name = user.username
            user.save()
        else:
            UsuarioPessoa.objects.create(user=user, pes_cod=pessoa)
            user.first_name = pessoa.pes_nome
            user.save()

        return user

#Formularios das Models, para verificação de duplicidade

class CargoFormulario(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'

    def clean_car_descricao(self):
        car_descricao = self.cleaned_data.get('car_descricao')
        if Cargo.objects.filter(car_descricao=car_descricao).exists():
            self.add_error('car_descricao', "Esse cargo já foi cadastrado anteriormente.")
        return car_descricao

class AreaPesquisaFormulario(forms.ModelForm):
    class Meta:
        model = AreaPesquisa
        fields = '__all__'

    def clean_ape_descricao(self):
        ape_descricao = self.cleaned_data.get('ape_descricao')
        if AreaPesquisa.objects.filter(ape_descricao=ape_descricao).exists():
            self.add_error('ape_descricao', "Essa Área de Pesquisa já foi cadastrado anteriormente.")
        return ape_descricao

class EstadoFormulario(forms.ModelForm):
    class Meta:
        model = Estado
        fields = '__all__'

    def clean_est_descricao(self):
        est_descricao = self.cleaned_data.get('est_descricao')
        if Estado.objects.filter(est_descricao=est_descricao).exists():
            self.add_error('est_descricao', "Esse Estado já foi cadastrado anteriormente.")
        return est_descricao

    def clean_est_sigla(self):
        est_sigla = self.cleaned_data.get('est_sigla')
        if Estado.objects.filter(est_sigla=est_sigla).exists():
            self.add_error('est_sigla', "Esse Sigla de Estado já foi cadastrado anteriormente.")
        return est_sigla

class CidadeFormulario(forms.ModelForm):
    class Meta:
        model = Cidade
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        cid_descricao = cleaned_data.get('cid_descricao')
        est_cod = cleaned_data.get('est_cod')
        if Cidade.objects.filter(cid_descricao=cid_descricao, est_cod=est_cod).exists():
            self.add_error('cid_descricao', "Essa Cidade vinculada a esse Estado já foi cadastrado anteriormente.")
        return cleaned_data

class AreaArtisticaFormulario(forms.ModelForm):
    class Meta:
        model = AreaArtistica
        fields = '__all__'

    def clean_are_descricao(self):
        are_descricao = self.cleaned_data.get('are_descricao')
        if AreaArtistica.objects.filter(are_descricao=are_descricao).exists():
            self.add_error('are_descricao', "Esse Campo Artístico já foi cadastrado anteriormente.")
        return are_descricao

class CursoFormulario(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'

    def clean_cur_descricao(self):
        cur_descricao = self.cleaned_data.get('cur_descricao')
        if Curso.objects.filter(cur_descricao=cur_descricao).exists():
            self.add_error('cur_descricao', "Esse Curso já foi cadastrado anteriormente.")
        return cur_descricao

class EscolaridadeFormulario(forms.ModelForm):
    class Meta:
        model = Escolaridade
        fields = '__all__'

    def clean_esc_descricao(self):
        esc_descricao = self.cleaned_data.get('esc_descricao')
        if Escolaridade.objects.filter(esc_descricao=esc_descricao).exists():
            self.add_error('esc_descricao', "Essa Escolaridade já foi cadastrada anteriormente.")
        return esc_descricao

class EtniaFormulario(forms.ModelForm):
    class Meta:
        model = Etnia
        fields = '__all__'

    def clean_etn_descricao(self):
        etn_descricao = self.cleaned_data.get('etn_descricao')
        if Etnia.objects.filter(etn_descricao=etn_descricao).exists():
            self.add_error('etn_descricao', "Essa Etinia/Raça já foi cadastrada anteriormente.")
        return etn_descricao

class GeneroFormulario(forms.ModelForm):
    class Meta:
        model = Genero
        fields = '__all__'

    def clean_gen_descricao(self):
        gen_descricao = self.cleaned_data.get('gen_descricao')
        if Genero.objects.filter(gen_descricao=gen_descricao).exists():
            self.add_error('gen_descricao', "Esso Gênero já foi cadastrado anteriormente.")
        return gen_descricao

class OrientacaoSexualFormulario(forms.ModelForm):
    class Meta:
        model = OrientacaoSexual
        fields = '__all__'

    def clean_ori_descricao(self):
        ori_descricao = self.cleaned_data.get('ori_descricao')
        if OrientacaoSexual.objects.filter(ori_descricao=ori_descricao).exists():
            self.add_error('ori_descricao', "Essa Orientação Sexual já foi cadastrada anteriormente.")
        return ori_descricao