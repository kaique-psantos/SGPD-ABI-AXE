from django.apps import apps
from django.contrib import admin
from .models import Cargo, AreaPesquisa, MembroDiretoria, Estado, Cidade, Endereco, Genero, Oficio, OrientacaoSexual, Escolaridade, Etnia, AreaArtistica, Evento, Bolsista, EventoXPessoa, Agenda, Pessoa, Pais
#Estado
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('est_descricao', 'est_sigla')
    search_fields = ('est_descricao',)
    ordering = ('est_descricao',)
    

admin.site.register(Estado, EstadoAdmin)

class PaisAdmin(admin.ModelAdmin):
    list_display = ('pai_descricao', 'pai_sigla', )
    search_fields = ('pai_descricao',)
    ordering = ('pai_descricao',)
    

admin.site.register(Pais, PaisAdmin)

#Cidade
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('cid_descricao', 'est_cod')
    search_fields = ('cid_descricao',)   
    ordering = ('cid_descricao',)

admin.site.register(Cidade, CidadeAdmin)

#Endereço
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('end_rua', 'end_bairro', 'cid_cod', 'est_cod')
    search_fields = ('cid_cod__cid_descricao',)
    ordering = ('cid_cod__cid_descricao',)
admin.site.register(Endereco, EnderecoAdmin)

#Genero
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('gen_descricao',)
    search_fields = ('gen_descricao',)
    ordering = ('gen_descricao',)
    
admin.site.register(Genero, GeneroAdmin)

#Orientação Sexual
class OrientacaoSexualAdmin(admin.ModelAdmin):
    list_display = ('ori_descricao',)
    search_fields = ('ori_descricao',)
    ordering = ('ori_descricao',)

admin.site.register(OrientacaoSexual, OrientacaoSexualAdmin)

#Escolaridade 
class EscolaridadeAdmin(admin.ModelAdmin):
    list_display = ('esc_descricao',)
    search_fields = ('esc_descricao',)
    ordering = ('esc_descricao',)

admin.site.register(Escolaridade, EscolaridadeAdmin)
#Etnia
class EtniaAdmin(admin.ModelAdmin):
    list_display = ('etn_descricao',)
    search_fields = ('etn_descricao',)
    ordering = ('etn_descricao',)

admin.site.register(Etnia, EtniaAdmin)

#AreaArtistica
class AreaArtisticaAdmin(admin.ModelAdmin):
    list_display = ('are_descricao', 'are_ativo',)
    search_fields = ('are_descricao',)
    ordering = ('are_descricao',)

admin.site.register(AreaArtistica, AreaArtisticaAdmin)
#Cargo
class CargoAdmin(admin.ModelAdmin):
    list_display = ('car_descricao', 'car_ativo')
    search_fields = ('car_descricao',)
    ordering = ('car_descricao',)

admin.site.register(Cargo, CargoAdmin)

#AreaPesquisa
class AreaPesquisaAdmin(admin.ModelAdmin):
    list_display = ('ape_descricao',)  
    search_fields = ('ape_descricao',)
    ordering = ('ape_descricao',)

admin.site.register(AreaPesquisa, AreaPesquisaAdmin)  

#Diretoria
class MembroDiretoriaAdmin(admin.ModelAdmin):
    list_display = ('pes_cod', 'car_cod', 'dir_data_inicio', 'dir_data_fim', 'dir_ativo')
    search_fields = ('pes_cod__pes_nome',)
    ordering = ('pes_cod__pes_nome',)

admin.site.register(MembroDiretoria, MembroDiretoriaAdmin)  

#Oficio
class OficioAdmin(admin.ModelAdmin):
    list_display = ('ofi_destinatario', 'ofi_assunto', 'ofi_numero', 'ofi_data', 'ofi_texto','dir_cod')
    search_fields = ('ofi_assunto',) #Precisa ser analisado
    ordering = ('ofi_assunto',)
admin.site.register(Oficio, OficioAdmin)  

#Bolsista
class BolsistaAdmin(admin.ModelAdmin):
    list_display = ('pes_cod', 'bol_data_inicio', 'bol_data_fim', 'ape_cod', 'bol_ativo')
    search_fields = ('pes_cod__pes_nome', )
    ordering = ('bol_data_inicio',)

admin.site.register(Bolsista, BolsistaAdmin)

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('pes_cod', 'pes_nome', 'pes_data_nascimento', 'pes_cpf', 'cid_naturalidade', 'est_naturalidade', 'end_cod', 'ori_cod', 'gen_cod', 'esc_cod', 'etn_cod', 'pes_data_ingresso', 'pes_data_saida', 'pes_ativo', 'are_cod')
    search_fields = ('pes_nome', 'pes_cpf', 'cid_naturalidade__nome', 'est_naturalidade__nome')
    ordering = ('pes_nome',)
    
admin.site.register(Pessoa, PessoaAdmin)   

#EventoAdmin
class EventoAdmin(admin.ModelAdmin):
    list_display = ('eve_nome', 'eve_data', 'cid_local', 'est_cod', 'eve_local_saida', 'eve_horario_saida', 'eve_local_chegada', 'eve_horario_chegada', 'eve_local_retorno', 'eve_horario_retorno', 'eve_data_retorno')
    search_fields = ('eve_nome',)
    ordering =  ('eve_data',)
    
admin.site.register(Evento, EventoAdmin)

#Evento - Pessoa
#A ser conversado
class EventoXPessoaAdmin(admin.ModelAdmin):
    list_display = ('eve_cod', 'pes_cod',)
    search_fields = ('eve_cod__eve_nome', 'pes_cod__pes_nome',)
    ordering =  ('eve_cod',)

admin.site.register(EventoXPessoa, EventoXPessoaAdmin)

#Agenda
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('age_descricao', 'age_data', 'eve_cod',)
    search_fields = ('age_descricao',)
    ordering = ('age_data',)
admin.site.register(Agenda, AgendaAdmin)


