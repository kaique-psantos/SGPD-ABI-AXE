from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout
from abi.models import Genero, OrientacaoSexual, Etnia, Escolaridade, AreaArtistica, Cidade, Estado, Pais, Pessoa
from .forms import PessoaForm
from abi.models import Genero, OrientacaoSexual, Etnia, Escolaridade, AreaArtistica, Cidade, Estado, Pais, Pessoa, Endereco
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

def index(request):
  context = {
    'segment': 'index'
  }
  return render(request, "pages/index.html", context)

#pessoa
def pessoa_view(request):
    import logging
    logger = logging.getLogger(__name__)
    generos = Genero.objects.all()
    orientacaoSexual = OrientacaoSexual.objects.all()
    etnia = Etnia.objects.all()
    escolaridade = Escolaridade.objects.all()
    areaArtistica = AreaArtistica.objects.all()
    cidade = Cidade.objects.all()
    estado = Estado.objects.all()
    pais = Pais.objects.all()

    context = {
        'generos': generos,
        'orientacaoSexual': orientacaoSexual,
        'etnia': etnia,
        'escolaridade': escolaridade,
        'areaArtistica': areaArtistica,
        'cidade': cidade,
        'estado': estado,
        'pais': pais,
    }

    if request.method == 'POST':
        # Campos do formulário
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        cidade_naturalidade_id = request.POST.get('cidade_naturalidade')
        estado_naturalidade_id = request.POST.get('estado_naturalidade')
        genero_id = request.POST.get('genero')
        orientacao_sexual_id = request.POST.get('orientacaoSexual')
        etnia_id = request.POST.get('etnia')
        escolaridade_id = request.POST.get('escolaridade')
        area_artistica_id = request.POST.get('areaArtistica')
        data_ingresso = request.POST.get('data_ingresso')

        # Campos adicionais
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        celular = request.POST.get('celular')

        # Campo de imagem
        imagem = request.FILES.get('imagem')

        logger.debug(f"Email recebido: {email}")

        if not email:
            messages.error(request, "O campo de email não pode estar vazio.")
            return render(request, 'pages/pessoa.html', context)

        # Obter objetos das FK
        cidade_naturalidade_obj = Cidade.objects.filter(cid_cod=cidade_naturalidade_id).first()
        estado_naturalidade_obj = Estado.objects.filter(est_cod=estado_naturalidade_id).first()
        genero_obj = Genero.objects.filter(gen_cod=genero_id).first()
        orientacao_sexual_obj = OrientacaoSexual.objects.filter(ori_cod=orientacao_sexual_id).first()
        etnia_obj = Etnia.objects.filter(etn_cod=etnia_id).first()
        escolaridade_obj = Escolaridade.objects.filter(esc_cod=escolaridade_id).first()
        area_artistica_obj = AreaArtistica.objects.filter(are_cod=area_artistica_id).first()

        if not data_ingresso:
            data_ingresso = timezone.now()

        cpf = ''.join(filter(str.isdigit, cpf))

        # Criando a pessoa com as FKs e a imagem
        pessoa = Pessoa(
            pes_nome=nome,
            pes_cpf=cpf,
            pes_data_nascimento=data_nascimento,
            cid_naturalidade=cidade_naturalidade_obj,
            est_naturalidade=estado_naturalidade_obj,
            gen_cod=genero_obj,
            ori_cod=orientacao_sexual_obj,
            etn_cod=etnia_obj,
            esc_cod=escolaridade_obj,
            are_cod=area_artistica_obj,
            pes_data_ingresso=data_ingresso,
            pes_email=email,
            pes_telefone=telefone,
            pes_celular=celular,
            pes_imagem=imagem
        )
        pessoa.save()

        # Capturando dados para o endereço
        cidade_id = request.POST.get('cidade')
        estado_id = request.POST.get('estado')

        cidade_obj = Cidade.objects.filter(cid_cod=cidade_id).first()
        estado_obj = Estado.objects.filter(est_cod=estado_id).first()

        if not cidade_obj:
            messages.error(request, "A cidade selecionada para o endereço não pode estar vazia.")
            return render(request, 'pages/pessoa.html', context)

        if not estado_obj:
            messages.error(request, "O estado selecionado para o endereço não pode estar vazio.")
            return render(request, 'pages/pessoa.html', context)

        # Criando o objeto Endereco
        endereco = Endereco(
            pessoa=pessoa,
            end_rua=request.POST.get('logradouro'),
            cid_cod=cidade_obj,
            est_cod=estado_obj,
            end_bairro=request.POST.get('bairro'),
            end_numero=request.POST.get('numero'),
            end_complemento=request.POST.get('complemento'),
            end_referencia=request.POST.get('referencia'),
        )
        endereco.save()

        # Atualizar a relação com o endereço
        pessoa.endereco = endereco
        pessoa.save()

        messages.success(request, 'Pessoa e endereço salvos com sucesso!')

        return redirect('pessoa')

    return render(request, 'pages/pessoa.html', context)

# Components
@login_required(login_url='/accounts/login/')
def bc_button(request):
  context = {
    'parent': 'basic_components',
    'segment': 'button'
  }
  return render(request, "pages/components/bc_button.html", context)

@login_required(login_url='/accounts/login/')
def bc_badges(request):
  context = {
    'parent': 'basic_components',
    'segment': 'badges'
  }
  return render(request, "pages/components/bc_badges.html", context)

@login_required(login_url='/accounts/login/')
def bc_breadcrumb_pagination(request):
  context = {
    'parent': 'basic_components',
    'segment': 'breadcrumbs_&_pagination'
  }
  return render(request, "pages/components/bc_breadcrumb-pagination.html", context)

@login_required(login_url='/accounts/login/')
def bc_collapse(request):
  context = {
    'parent': 'basic_components',
    'segment': 'collapse'
  }
  return render(request, "pages/components/bc_collapse.html", context)

@login_required(login_url='/accounts/login/')
def bc_tabs(request):
  context = {
    'parent': 'basic_components',
    'segment': 'navs_&_tabs'
  }
  return render(request, "pages/components/bc_tabs.html", context)

@login_required(login_url='/accounts/login/')
def bc_typography(request):
  context = {
    'parent': 'basic_components',
    'segment': 'typography'
  }
  return render(request, "pages/components/bc_typography.html", context)

@login_required(login_url='/accounts/login/')
def icon_feather(request):
  context = {
    'parent': 'basic_components',
    'segment': 'feather_icon'
  }
  return render(request, "pages/components/icon-feather.html", context)


# Forms and Tables
@login_required(login_url='/accounts/login/')
def form_elements(request):
  context = {
    'parent': 'form_components',
    'segment': 'form_elements'
  }
  return render(request, 'pages/form_elements.html', context)

@login_required(login_url='/accounts/login/')
def basic_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'basic_tables'
  }
  return render(request, 'pages/tbl_bootstrap.html', context)

# Chart and Maps
@login_required(login_url='/accounts/login/')
def morris_chart(request):
  context = {
    'parent': 'chart',
    'segment': 'morris_chart'
  }
  return render(request, 'pages/chart-morris.html', context)

@login_required(login_url='/accounts/login/')
def google_maps(request):
  context = {
    'parent': 'maps',
    'segment': 'google_maps'
  }
  return render(request, 'pages/map-google.html', context)

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
  context = {
    'segment': 'profile',
  }
  return render(request, 'pages/profile.html', context)

@login_required(login_url='/accounts/login/')
def sample_page(request):
  context = {
    'segment': 'sample_page',
  }
  return render(request, 'pages/sample-page.html', context)


