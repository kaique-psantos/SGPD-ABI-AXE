import random
import plotly.graph_objects as go
from django.db.models import Count, Avg
from ..models import Pessoa
from datetime import date



def get_random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_chart_colors(data_count):
    main_colors = ['#1DE9B6', '#1DC4E9', '#04A9F5', '#A389D4', '#F1F1F1', '#5C6BC0', '#FF4081', '#FF7043', '#80DEEA', '#D4E157', '#FFF176']
    
    colors = []

    if data_count <= len(main_colors):
        colors = main_colors[:data_count]
    else:
        colors = main_colors[:]
        random_colors_needed = data_count - len(main_colors)
        for _ in range(random_colors_needed):
            colors.append(get_random_color())
    
    return colors

def chartGeneros():
    generos = Pessoa.objects.filter(pes_ativo=True).values('gen_cod__gen_descricao').annotate(count=Count('gen_cod'))
    
    labels = [item['gen_cod__gen_descricao'] for item in generos]
    values = [item['count'] for item in generos]

    chart_colors = get_chart_colors(len(generos))

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, marker=dict(colors=chart_colors))])
    fig.update_layout(
        title_text='Gênero',
        width=300, 
        height=300,
        showlegend=False, 
        margin=dict(t=60, b=60, l=60, r=60),
    )

    grafico = fig.to_html(full_html=False, config={'displayModeBar': False})
    
    return grafico

def chartEtnias():
    etnias = Pessoa.objects.filter(pes_ativo=True).values('etn_cod__etn_descricao').annotate(count=Count('etn_cod'))
    
    labels = [item['etn_cod__etn_descricao'] for item in etnias]
    values = [item['count'] for item in etnias]

    chart_colors = get_chart_colors(len(etnias))

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, marker=dict(colors=chart_colors))])
    fig.update_layout(
        title_text='Etnia/Raça',
        width=300, 
        height=300,
        showlegend=False, 
        margin=dict(t=60, b=60, l=60, r=60),
    )

    grafico = fig.to_html(full_html=False, config={'displayModeBar': False})
    
    return grafico

def chartSexualidades():
    sexualidades = Pessoa.objects.filter(pes_ativo=True).values('ori_cod__ori_descricao').annotate(count=Count('ori_cod'))
    
    labels = [item['ori_cod__ori_descricao'] for item in sexualidades]
    values = [item['count'] for item in sexualidades]

    chart_colors = get_chart_colors(len(sexualidades))

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, marker=dict(colors=chart_colors))])
    fig.update_layout(
        title_text='Orientação Sexual',
        width=300, 
        height=300,
        showlegend=False, 
        margin=dict(t=60, b=60, l=60, r=60),
    )

    grafico = fig.to_html(full_html=False, config={'displayModeBar': False})
    
    return grafico

def chartMembroCampoArtistico():
    artistico = Pessoa.objects.filter(pes_ativo=True).values('are_cod__are_descricao').annotate(count=Count('are_cod'))

    labels = [item['are_cod__are_descricao'] for item in artistico]
    values = [item['count'] for item in artistico]
    
    chart_colors = get_chart_colors(len(artistico))
    
    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker=dict(color=chart_colors))])
    fig.update_layout(
        title_text='',
        height=300,
        xaxis_title="Campo Artistico",
        yaxis_title="Quantidade",
        margin=dict(t=40, b=40, l=40, r=40),
        dragmode = 'pan',

    )
    grafico = fig.to_html(full_html=False, config={'displayModeBar': False})
    
    return grafico

def calcular_media_idade():
    data_atual = date.today()
    pessoas = Pessoa.objects.all().filter(pes_ativo=True)
    
    idades = [
        (data_atual.year - pessoa.pes_data_nascimento.year - ((data_atual.month, data_atual.day) < (pessoa.pes_data_nascimento.month, pessoa.pes_data_nascimento.day)))
        for pessoa in pessoas
    ]
    
    media_idade = sum(idades) / len(idades) if idades else 0
    
    return media_idade