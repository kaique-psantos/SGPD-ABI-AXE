from django.apps import apps
from django.contrib import admin
from .models import *
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import format_html



class CustomModelAdmin(admin.ModelAdmin):
    def history_view(self, request, object_id, extra_context=None):
        obj = get_object_or_404(self.model, pk=object_id)
        extra_context = extra_context or {}
        extra_context['object_title'] = obj  
        
        return super().history_view(request, object_id, extra_context=extra_context)

#Estado
class EstadoAdmin(CustomModelAdmin):
    list_display = ('est_descricao', 'est_sigla')
    search_fields = ('est_descricao',)
    ordering = ('est_descricao',)
    

admin.site.register(Estado, EstadoAdmin)

#Cidade
class CidadeAdmin(CustomModelAdmin):
    list_display = ('cid_descricao', 'est_cod')
    search_fields = ('cid_descricao',)   
    ordering = ('cid_descricao',)

admin.site.register(Cidade, CidadeAdmin)

#Endereço
class EnderecoAdmin(CustomModelAdmin):
    list_display = ('end_rua', 'end_bairro', 'cid_cod', 'est_cod')
    search_fields = ('cid_cod__cid_descricao',)
    ordering = ('cid_cod__cid_descricao',)
admin.site.register(Endereco, EnderecoAdmin)

#Genero
class GeneroAdmin(CustomModelAdmin):
    list_display = ('gen_descricao',)
    search_fields = ('gen_descricao',)
    ordering = ('gen_descricao',)
    
admin.site.register(Genero, GeneroAdmin)

#Orientação Sexual
class OrientacaoSexualAdmin(CustomModelAdmin):
    list_display = ('ori_descricao',)
    search_fields = ('ori_descricao',)
    ordering = ('ori_descricao',)

admin.site.register(OrientacaoSexual, OrientacaoSexualAdmin)

#Escolaridade 
class EscolaridadeAdmin(CustomModelAdmin):
    list_display = ('esc_descricao',)
    search_fields = ('esc_descricao',)
    ordering = ('esc_descricao',)

admin.site.register(Escolaridade, EscolaridadeAdmin)
#Etnia
class EtniaAdmin(CustomModelAdmin):
    list_display = ('etn_descricao',)
    search_fields = ('etn_descricao',)
    ordering = ('etn_descricao',)

admin.site.register(Etnia, EtniaAdmin)

#AreaArtistica
class AreaArtisticaAdmin(CustomModelAdmin):
    list_display = ('are_descricao', 'are_ativo',)
    search_fields = ('are_descricao',)
    ordering = ('are_descricao',)

admin.site.register(AreaArtistica, AreaArtisticaAdmin)
#Cargo
class CargoAdmin(CustomModelAdmin):
    list_display = ('car_descricao', 'car_ativo')
    search_fields = ('car_descricao',)
    ordering = ('car_descricao',)
    
    def history_view(self, request, object_id, extra_context=None):
      
        obj = get_object_or_404(Cargo, pk=object_id)
        extra_context = extra_context or {}
        extra_context['object_title'] = obj  
        
        
        return super().history_view(request, object_id, extra_context=extra_context)

admin.site.register(Cargo, CargoAdmin)

#AreaPesquisa
class AreaPesquisaAdmin(CustomModelAdmin):
    list_display = ('ape_descricao',)  
    search_fields = ('ape_descricao',)
    ordering = ('ape_descricao',)

admin.site.register(AreaPesquisa, AreaPesquisaAdmin)  

#Diretoria
class MembroDiretoriaAdmin(CustomModelAdmin):
    list_display = ('pes_cod', 'dir_data_inicio', 'dir_data_fim', 'car_cod', 'dir_ativo')
    search_fields = ('pes_cod__pes_nome',)
    ordering = ('pes_cod__pes_nome',)

admin.site.register(MembroDiretoria, MembroDiretoriaAdmin)  

#Oficio
class OficioAdmin(CustomModelAdmin):
    list_display = ('ofi_numero', 'ofi_assunto', 'ofi_destinatario', 'ofi_data', 'dir_cod', 'botao_impressao')
    search_fields = ('ofi_assunto',) #Precisa ser analisado
    ordering = ('-ofi_data',)
    
    def botao_impressao(self, obj):
        url = reverse('oficio_imprimir', args=[obj.ofi_cod])
        return format_html('<a class="btn" href="{}"><i class="fa-solid fa-print"></i></a>', url)

    botao_impressao.short_description = 'Impressão'
admin.site.register(Oficio, OficioAdmin)  

#Bolsista
class BolsistaAdmin(CustomModelAdmin):
    list_display = ('pes_cod', 'bol_data_inicio', 'bol_data_fim', 'bol_ativo', 'ape_cod')
    search_fields = ('pes_cod__pes_nome', )
    ordering = ('bol_data_inicio',)

admin.site.register(Bolsista, BolsistaAdmin)

#EventoAdmin
class EventoAdmin(CustomModelAdmin):
    list_display = ('eve_nome', 'eve_data', 'cid_local', 'est_cod')
    search_fields = ('eve_nome',)
    ordering =  ('-eve_data',)
    

    
admin.site.register(Evento, EventoAdmin)

#Evento - Pessoa
#A ser conversado
class EventoXPessoaAdmin(CustomModelAdmin):
    list_display = ('eve_cod', 'pes_cod',)
    search_fields = ('eve_cod__eve_nome', 'pes_cod__pes_nome',)
    ordering =  ('eve_cod',)

admin.site.register(EventoXPessoa, EventoXPessoaAdmin)

#Agenda
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('age_titulo', 'age_data', 'eve_cod')
    search_fields = ('age_titulo',)
    ordering = ('-age_data',)
admin.site.register(Agenda, AgendaAdmin)


#Pessoa
admin.site.register(Pessoa)

class OficineiroAdmin(CustomModelAdmin):
    list_display = ('pes_cod', 'ofc_descricao', 'ofc_ativo',)
    search_fields = ('ofc_descricao',)
    ordering = ('pes_cod',)
admin.site.register(Oficineiro, OficineiroAdmin)


class CursoAdmin(CustomModelAdmin):
    list_display = ('cur_descricao', 'cur_ativo',)
    search_fields = ('cur_descricao',)
    ordering = ('cur_descricao',)
admin.site.register(Curso, CursoAdmin)