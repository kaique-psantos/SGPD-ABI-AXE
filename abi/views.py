from django.shortcuts import render, redirect
from django.utils import timezone
from .models import *
from django.urls import reverse
from .functions.charts import *
import math
import os
from django.http import HttpResponse
from django.db.models import F , Func
import locale
from admin_abi.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from templates import *
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone

@login_required
def index(request):

  context = {
    'segment'  : 'index',
  }
  return render(request, "pages/index.html", context)

@login_required
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
    
@login_required
def deletar_pessoa(request, pk):
    pessoa = get_object_or_404(Pessoa, pk=pk)
    pessoa.delete()
    return redirect(reverse('admin:abi_pessoa_changelist'))
@login_required
def pessoa_detail(request, pes_cod):
    pessoa = get_object_or_404(Pessoa, pes_cod=pes_cod)

    # Buscar todas as listas necessárias
    generos = Genero.objects.all()
    orientacaoSexual = OrientacaoSexual.objects.all()
    etnia = Etnia.objects.all()
    escolaridade = Escolaridade.objects.all()
    areaArtistica = AreaArtistica.objects.all()
    cidade = Cidade.objects.all()
    estado = Estado.objects.all()
    pais = Pais.objects.all()

    context = {
        'pessoa': pessoa,
        'generos': generos,
        'orientacaoSexual': orientacaoSexual,
        'etnia': etnia,
        'escolaridade': escolaridade,
        'areaArtistica': areaArtistica,
        'cidade': cidade,
        'estado': estado,
        'pais': pais,
    }
    return render(request, 'pages/pessoa.html', context)


@login_required
def pessoa_view(request):
    import logging
    logger = logging.getLogger(__name__)

    # Carregar listas para popular o template
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
        pessoa_id = request.POST.get('pessoa_id', '')  # Vem do input hidden se for edição

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

        # Endereço
        logradouro = request.POST.get('logradouro')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        complemento = request.POST.get('complemento')
        referencia = request.POST.get('referencia')
        cidade_id = request.POST.get('cidade')
        estado_id = request.POST.get('estado')

        logger.debug(f"Dados recebidos: Nome: {nome}, CPF: {cpf}, Email: {email}, ... pessoa_id: {pessoa_id}")

        # Validar campos obrigatórios (para ambos os casos - criar/editar)
        if not (
            nome and cpf and data_nascimento and cidade_naturalidade_id
            and estado_naturalidade_id and genero_id and orientacao_sexual_id
            and etnia_id and escolaridade_id 
            and logradouro and bairro and numero and cidade_id and estado_id
        ):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            # Se estiver editando, precisamos recolocar 'pessoa' no context para re-renderizar corretamente
            if pessoa_id:
                pessoa_atual = Pessoa.objects.filter(pes_cod=pessoa_id).first()
                context['pessoa'] = pessoa_atual
            return render(request, 'pages/pessoa.html', context)

        # Obter instâncias FK
        cidade_naturalidade_obj = Cidade.objects.filter(cid_cod=cidade_naturalidade_id).first()
        estado_naturalidade_obj = Estado.objects.filter(est_cod=estado_naturalidade_id).first()
        genero_obj = Genero.objects.filter(gen_cod=genero_id).first()
        orientacao_sexual_obj = OrientacaoSexual.objects.filter(ori_cod=orientacao_sexual_id).first()
        etnia_obj = Etnia.objects.filter(etn_cod=etnia_id).first()
        escolaridade_obj = Escolaridade.objects.filter(esc_cod=escolaridade_id).first()
        area_artistica_obj = AreaArtistica.objects.filter(are_cod=area_artistica_id).first()
        cidade_obj = Cidade.objects.filter(cid_cod=cidade_id).first()
        estado_obj = Estado.objects.filter(est_cod=estado_id).first()

        # Se o data_ingresso não vier no POST, use a data/hora atual
        if not data_ingresso:
            data_ingresso = timezone.now()

        # Normalizar CPF (remover pontuação)
        cpf = ''.join(filter(str.isdigit, cpf))

        try:
            if pessoa_id:  # ----------- EDIÇÃO -----------
                pessoa = get_object_or_404(Pessoa, pes_cod=pessoa_id)
                # Atualiza os campos
                pessoa.pes_nome = nome
                pessoa.pes_cpf = cpf
                pessoa.pes_data_nascimento = data_nascimento
                pessoa.cid_naturalidade = cidade_naturalidade_obj
                pessoa.est_naturalidade = estado_naturalidade_obj
                pessoa.gen_cod = genero_obj
                pessoa.ori_cod = orientacao_sexual_obj
                pessoa.etn_cod = etnia_obj
                pessoa.esc_cod = escolaridade_obj
                pessoa.are_cod = area_artistica_obj
                pessoa.pes_data_ingresso = data_ingresso
                pessoa.pes_email = email
                pessoa.pes_telefone = telefone
                pessoa.pes_celular = celular
                if imagem:
                    pessoa.pes_imagem = imagem
                pessoa.end_rua = logradouro
                pessoa.cid_cod = cidade_obj
                pessoa.est_cod = estado_obj
                pessoa.end_bairro = bairro
                pessoa.end_numero = numero
                pessoa.end_complemento = complemento
                pessoa.end_referencia = referencia

            else:  # ----------- CRIAÇÃO -----------
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

            # Salvar (funciona para novo OU edição)
            pessoa.save()
            
            if pessoa_id:
                registrar_log_admin(request.user, pessoa, ADDITION, 'Adicionou via custom view')
            else:
                registrar_log_admin(request.user, pessoa, CHANGE, 'Alterou via custom view')

            # messages.success(request, 'Pessoa e endereço salvos com sucesso!')
            return redirect('admin:abi_pessoa_changelist')
        except Exception as e:
            logger.error(f"Erro ao salvar a pessoa: {e}")
            messages.error(request, f"Erro ao salvar a pessoa: {e}")
            # Em caso de erro, se for edição, reenvie a instância pro template
            if pessoa_id:
                context['pessoa'] = pessoa
            return render(request, 'pages/pessoa.html', context)

    # Se GET, apenas renderiza o form em branco ou com dados do context
    return render(request, 'pages/pessoa.html', context)


def verificar_cpf(request):
    cpf = request.GET.get('cpf')
    pes_cod = request.GET.get('pes_cod', None)  
    
    cpf = cpf.replace('.', '').replace('-', '')
    
    qs = Pessoa.objects.filter(pes_cpf=cpf)
    
    if pes_cod:
        qs = qs.exclude(pes_cod=pes_cod)

    existe = qs.exists()
    return JsonResponse({"existe": existe})

def registrar_log_admin(user, obj, action_flag, change_message=''):
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=str(obj),
        action_flag=action_flag,
        change_message=change_message
    )
    
    
    from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

@login_required
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

    ofi_data = oficio['ofi_data']
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    data_formatada = ofi_data.strftime('%d de %B de %Y')
    data_completa = f"Delmiro Gouveia - AL, {data_formatada}"

    context = {
        'ofi_numero': oficio['ofi_numero'],
        'ofi_data': data_completa,
        'ofi_destinatario': oficio['ofi_destinatario'],
        'ofi_texto': oficio['ofi_texto'],
        'nome': oficio['pes_nome'],
        'cargo': oficio['car_descricao'],
        'cpf': oficio['cpf'],
        'ofi_assunto': oficio['ofi_assunto'],
    }

 
    html_content = render_to_string('pages/oficio.html', context)

    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = 'inline; filename="oficio.html"'

    return response