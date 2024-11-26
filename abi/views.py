from django.shortcuts import render
from django.utils import timezone
from .models import *
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
        response['Content-Disposition'] = f'attachment; filename="oficio_{oficio['ofi_assunto']}.pdf"'
        return response

