from django.shortcuts import render
from django.db.models import Count
from .models import *
from .charts import *
from .functions.instagram import *
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
    
    context = {
        'segment'  : 'dashboard',
        'integrantes_ativos': integrantes_ativos,
        'porcentagem_ativos': math.trunc(porcentagem_ativos),
        'bolsistas_ativos': bolsistas_ativos,
        'generos': chartGeneros(),
        'etnias': chartEtnias(),
        'sexualidades': chartSexualidades(),
        'instagram': get_instagram_followers(),
    }
    
    return render(request, 'pages/dashboard.html', context)