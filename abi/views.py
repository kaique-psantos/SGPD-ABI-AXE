from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
import re
from django.urls import reverse
from .functions.charts import *
import plotly.graph_objects as go
import math
import os
from django.conf import settings
from django.http import HttpResponse
from pyreportjasper import PyReportJasper
from django.db.models import F, Value, Func
from datetime import datetime
import locale
from admin_abi.forms import *
from abi.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from abi.templates import *

from django.http import JsonResponse

from abi.models import Genero, OrientacaoSexual, Etnia, Escolaridade, AreaArtistica, Cidade, Estado, Pais, Pessoa, Endereco
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from admin_abi.forms import PessoaForm

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def index(request):

  context = {
    'segment'  : 'index',
  }
  return render(request, "pages/index.html", context)

def dashboard(request):
    integrantes_ativos = Pessoa.objects.filter(pes_ativo=True).count()
    total_integrantes = Pessoa.objects.count()
    porcentagem_ativos = (integrantes_ativos / total_integrantes) * 100 if total_integrantes > 0 else 0
    
    bolsistas_ativos = Bolsista.objects.filter(bol_ativo=True).count()
    # diretoria = MembroDiretoria.objects.filter(dir_ativo=True).count()
    oficineiros_ativos = Oficineiro.objects.filter(ofc_ativo=True).count()
    oficineiros_total = Oficineiro.objects.count()
    oficineiros_porcentagem = (oficineiros_ativos / oficineiros_total) * 100 if oficineiros_total > 0 else 0
    
    hoje = timezone.now().date()
    proximos_eventos = Evento.objects.filter(eve_data__gte=hoje).order_by('eve_data')[:5]
    
    context = {
        'segment'  : 'index',
        'integrantes_ativos': integrantes_ativos,
        'porcentagem_ativos': math.trunc(porcentagem_ativos),
        'bolsistas_ativos': bolsistas_ativos,
        'generos': chartGeneros(),
        'etnias': chartEtnias(),
        'sexualidades': chartSexualidades(),
        'membros_artistico': chartMembroCampoArtistico(),
        'proximos_eventos': proximos_eventos,
        'oficineiros': oficineiros_ativos,
        'oficineiros_porcentagem': math.trunc(oficineiros_porcentagem),
    }
    
    return render(request, 'pages/dashboard.html', context)
  
def page_not_found(request, exception):
    return render(request, 'pages/404.html')
  
def error_403(request, exception):
    return render(request, 'pages/403.html')
  
class FormatCPF(Func):
    function = 'formatar_cpf'

def deletar_pessoa(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    pessoa.delete()
    return redirect(reverse('admin:abi_pessoa_changelist'))

def pessoa_detail(request, pes_cod):
    pessoa = get_object_or_404(Pessoa, pes_cod=pes_cod)
    return render(request, 'pages/pessoa.html', {'pessoa': pessoa})


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

        # Capturando dados para o endereço
        logradouro = request.POST.get('logradouro')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')
        referencia = request.POST.get('referencia')
        cidade_id = request.POST.get('cidade')
        estado_id = request.POST.get('estado')

        logger.debug(f"Dados recebidos: Nome: {nome}, CPF: {cpf}, Email: {email}, Cidade Naturalidade: {cidade_naturalidade_id}, Estado Naturalidade: {estado_naturalidade_id}, Genero: {genero_id}, Orientacao Sexual: {orientacao_sexual_id}, Etnia: {etnia_id}, Escolaridade: {escolaridade_id}, Area Artistica: {area_artistica_id}, Data Ingresso: {data_ingresso}, Logradouro: {logradouro}, Bairro: {bairro}, Numero: {numero}, Complemento: {complemento}, Referencia: {referencia}, Cidade: {cidade_id}, Estado: {estado_id}")

        # Verificações de campos obrigatórios
        if not nome or not cpf or not data_nascimento or not cidade_naturalidade_id or not estado_naturalidade_id or not genero_id or not orientacao_sexual_id or not etnia_id or not escolaridade_id or not area_artistica_id or not logradouro or not bairro or not numero or not cidade_id or not estado_id:
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'pages/pessoa.html', context)

        # Obter objetos das FK
        cidade_naturalidade_obj = Cidade.objects.filter(cid_cod=cidade_naturalidade_id).first()
        estado_naturalidade_obj = Estado.objects.filter(est_cod=estado_naturalidade_id).first()
        genero_obj = Genero.objects.filter(gen_cod=genero_id).first()
        orientacao_sexual_obj = OrientacaoSexual.objects.filter(ori_cod=orientacao_sexual_id).first()
        etnia_obj = Etnia.objects.filter(etn_cod=etnia_id).first()
        escolaridade_obj = Escolaridade.objects.filter(esc_cod=escolaridade_id).first()
        area_artistica_obj = AreaArtistica.objects.filter(are_cod=area_artistica_id).first()
        cidade_obj = Cidade.objects.filter(cid_cod=cidade_id).first()
        estado_obj = Estado.objects.filter(est_cod=estado_id).first()

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
            pes_imagem=imagem,
            end_rua=logradouro,
            cid_cod=cidade_obj,
            est_cod=estado_obj,
            end_bairro=bairro,
            end_numero=numero,
            end_complemento=complemento,
            end_referencia=referencia,
        )
        try:
            pessoa.save()
            messages.success(request, 'Pessoa e endereço salvos com sucesso!')
            return redirect('admin:abi_pessoa_changelist')
        except Exception as e:
            logger.error(f"Erro ao salvar a pessoa: {e}")
            messages.error(request, f"Erro ao salvar a pessoa: {e}")
            return render(request, 'pages/pessoa.html', context)

    return render(request, 'pages/pessoa.html', context)

def verificar_cpf(request):
    cpf = request.GET.get('cpf', '')

    # Remove o caracteres
    cpf_limpo = re.sub(r'\D', '', cpf)
    
    # Verifica se o CPF já existe no banco de dados
    if Pessoa.objects.filter(pes_cpf=cpf_limpo).exists():
        return JsonResponse({'existe': True})
    
    return JsonResponse({'existe': False})

def imprimir_oficio(request, ofi_cod):
    
    oficio = Oficio.objects.filter(ofi_cod=ofi_cod).select_related('dir_cod__pes_cod', 'dir_cod__car_cod').annotate(
            pes_nome=F('dir_cod__pes_cod__pes_nome'),
            car_descricao=F('dir_cod__car_cod__car_descricao'),
            cpf=F('dir_cod__pes_cod__pes_cpf')
        ).values(
            'ofi_destinatario',
            'ofi_assunto',
            'ofi_numero',
            'ofi_data',
            'ofi_texto',
            'pes_nome',
            'car_descricao',
            'cpf'
        ).first()

    jasper_file = os.path.join(settings.MEDIA_ROOT, 'reports', 'Oficio.jasper')
    output_file = os.path.join(settings.MEDIA_ROOT, 'reports/temp', f"oficio_{oficio['ofi_assunto']}.pdf")
    
    ofi_data = oficio['ofi_data']
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    data_formatada = ofi_data.strftime('%d de %B de %Y')
    teste =  "Delmiro Gouveia - AL, "+ data_formatada
    

    parametros = {
        'ofi_numero': oficio['ofi_numero'],
        'ofi_data':  teste,
        'ofi_destinatario': oficio['ofi_destinatario'],
        'ofi_texto': oficio['ofi_texto'],
        'nome': oficio['pes_nome'],
        'cargo': oficio['car_descricao'],
        'cpf': oficio['cpf'],
        'ofi_assunto': oficio['ofi_assunto'],
    }

    jasper = PyReportJasper()

    jasper.config(
        input_file=jasper_file,
        output_file=output_file,
        output_formats=["pdf"],
        locale='pt_BR',
        parameters=parametros,
    )

    jasper.process_report()

    with open(output_file, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f"attachment; filename='oficio_{oficio['ofi_assunto']}.pdf'"
        return response

