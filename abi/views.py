from django.shortcuts import render
from django.utils import timezone
from .models import *
from .functions.charts import *
import plotly.graph_objects as go
import math

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