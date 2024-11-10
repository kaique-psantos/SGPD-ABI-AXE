from django.shortcuts import render
from django.db.models import Count
from .models import *
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
    diretoria = MembroDiretoria.objects.filter(dir_ativo=True).count()
    
    
    context = {
        'segment'  : 'dashboard',
        'integrantes_ativos': integrantes_ativos,
        'porcentagem_ativos': math.trunc(porcentagem_ativos),
        'bolsistas_ativos': bolsistas_ativos,
        'diretoria_total': diretoria,
        'generos':chartGeneros(),
        'etnias':chartEtnias(),
        'sexualidades':chartSexualidades(),
    }
    
    return render(request, 'pages/dashboard.html', context)


def chartGeneros():

    generos = Pessoa.objects.values('gen_cod__gen_descricao').annotate(count=Count('gen_cod'))
    
    labels = [item['gen_cod__gen_descricao'] for item in generos]
    values = [item['count'] for item in generos]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(
      title_text='Gênero',
      width=300, 
      height=300,
      showlegend=False, 
      margin=dict(t=60, b=60, l=60, r=60),
      )

    graph_html = fig.to_html(full_html=False, config={'displayModeBar': False})
    
    return graph_html

def chartEtnias():
  etnias = Pessoa.objects.values('etn_cod__etn_descricao').annotate(count=Count('etn_cod'))
  
  labels = [item['etn_cod__etn_descricao'] for item in etnias]
  values = [item['count'] for item in etnias]

  fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
  fig.update_layout(
      title_text='Etnia/Raça',
      width=300, 
      height=300,
      showlegend=False, 
      margin=dict(t=60, b=60, l=60, r=60),

      )

  graph_html = fig.to_html(full_html=False, config={'displayModeBar': False})
    
  return graph_html

def chartSexualidades():
  sexualidades = Pessoa.objects.values('ori_cod__ori_descricao').annotate(count=Count('ori_cod'))
  
  labels = [item['ori_cod__ori_descricao'] for item in sexualidades]
  values = [item['count'] for item in sexualidades]

  fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
  fig.update_layout(
      title_text='Orientação Sexual',
      width=300, 
      height=300,
      showlegend=False, 
      margin=dict(t=60, b=60, l=60, r=60),

      )

  graph_html = fig.to_html(full_html=False, config={'displayModeBar': False})
    
  return graph_html