from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import datetime


class Estado(models.Model):
    est_cod = models.AutoField(primary_key=True)
    est_descricao = models.CharField(max_length=100, verbose_name="Estado")
    est_sigla =  models.CharField(max_length=2, verbose_name="Sigla do Estado")
    

    def __str__(self):
        return self.est_sigla

class Pais(models.Model):
    pai_cod = models.AutoField(primary_key=True)
    pai_sigla =  models.CharField(max_length=2, verbose_name="Sigla do País")
    pai_descricao = models.CharField(max_length=100, verbose_name="País")

    def __str__(self):
        return self.pai_sigla
class Cidade(models.Model):
    cid_cod = models.AutoField(primary_key=True)
    cid_descricao = models.CharField(max_length=255, verbose_name="Cidade")
    est_cod = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")

    def __str__(self):
        return self.cid_descricao

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"

class Endereco(models.Model):
    end_cod = models.AutoField(primary_key=True)
    cid_cod = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name = "Cidade")
    est_cod = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado")
    end_rua = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Rua")
    end_bairro = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Bairro")
    end_numero = models.CharField(max_length=10, null=True, blank=True, verbose_name = "Numero")
    end_complemento = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Complemento")
    end_referencia = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Referência")

    def __str__(self):
        return f"{self.end_rua}, {self.end_numero}"

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

class Genero(models.Model):
    gen_cod = models.AutoField(primary_key=True)
    gen_descricao = models.CharField(max_length=255, verbose_name = "Gênero")

    def __str__(self):
        return self.gen_descricao

    class Meta:
        verbose_name = "Gênero"
        verbose_name_plural = "Gêneros"

class OrientacaoSexual(models.Model):
    ori_cod = models.AutoField(primary_key=True)
    ori_descricao = models.CharField(max_length=255, verbose_name = "Orientação Sexual")

    def __str__(self):
        return self.ori_descricao

    class Meta:
        verbose_name = "Orientação Sexual"
        verbose_name_plural = "Orientações Sexuais"

class Escolaridade(models.Model):
    esc_cod = models.AutoField(primary_key=True)
    esc_descricao = models.CharField(max_length=255, verbose_name = "Escolaridade")

    def __str__(self):
        return self.esc_descricao

    class Meta:
        verbose_name = "Escolaridade"
        verbose_name_plural = "Escolaridades"

class Etnia(models.Model):
    etn_cod = models.AutoField(primary_key=True)
    etn_descricao = models.CharField(max_length=255, verbose_name = "Etnia/Raça")

    def __str__(self):
        return self.etn_descricao

    class Meta:
        verbose_name = "Etnia/Raça"
        verbose_name_plural = "Etnias/Raças"

class AreaArtistica(models.Model):
    are_cod = models.AutoField(primary_key=True)
    are_descricao = models.CharField(max_length=255, verbose_name = "Campo Artistico")
    are_ativo = models.BooleanField(default=True, verbose_name = "Ativo")

    def __str__(self):
        return self.are_descricao

    class Meta:
        verbose_name = "Campo Artistico"
        verbose_name_plural = "Campo Artistico"

class Curso(models.Model):
    cur_cod = models.AutoField(primary_key=True)
    cur_descricao = models.CharField(max_length=255, verbose_name = "Curso")
    cur_ativo = models.BooleanField(default=True, verbose_name = "Ativo")

    def __str__(self):
        return self.cur_descricao


class Pessoa(models.Model):
    pes_cod = models.AutoField(primary_key=True)
    pes_nome = models.CharField(max_length=255, verbose_name="Nome")
    pes_data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    pes_cpf = models.CharField(max_length=11, verbose_name="CPF")
    pes_email = models.CharField(max_length=255, verbose_name="E-mail")
    pes_telefone = models.CharField(max_length=15, verbose_name="Telefone")
    pes_celular = models.CharField(max_length=15, verbose_name="Celular")
    cid_naturalidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL,blank=True, null=True, related_name='naturalidade', verbose_name="Cidade")
    est_naturalidade = models.ForeignKey(Estado, on_delete=models.SET_NULL, blank=True, null=True, related_name='naturalidade', verbose_name="Estado")
    end_cod = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, verbose_name="Endereço")
    ori_cod = models.ForeignKey(OrientacaoSexual, on_delete=models.SET_NULL, null=True, verbose_name="Orientação Sexual")
    gen_cod = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, verbose_name="Gênero")
    esc_cod = models.ForeignKey(Escolaridade, on_delete=models.SET_NULL, null=True, verbose_name="Escolaridade")
    etn_cod = models.ForeignKey(Etnia, on_delete=models.SET_NULL, null=True, verbose_name="Etnia")
    pes_data_ingresso = models.DateField(verbose_name="Data de Ingresso")
    pes_data_saida = models.DateField(null=True, blank=True, verbose_name="Data de Saída")
    pes_ativo = models.BooleanField(default=True, verbose_name="Ativo")
    are_cod = models.ForeignKey(AreaArtistica, on_delete=models.SET_NULL, null=True, verbose_name="Área Artistica")
    pes_imagem = models.ImageField(upload_to='imagens/integrantes/', null=True, blank=True, verbose_name="Imagem")
    cid_cod = models.ForeignKey(Cidade, on_delete=models.CASCADE, verbose_name="Cidade", default=1)  # Valor padrão adicionado
    est_cod = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado", default=1)  # Valor padrão adicionado
    end_rua = models.CharField(max_length=255, null=True, blank=True, verbose_name="Rua")
    end_bairro = models.CharField(max_length=255, null=True, blank=True, verbose_name="Bairro")
    end_numero = models.CharField(max_length=10, null=True, blank=True, verbose_name="Número")
    end_complemento = models.CharField(max_length=255, null=True, blank=True, verbose_name="Complemento")
    end_referencia = models.CharField(max_length=255, null=True, blank=True, verbose_name="Referência")

    def __str__(self):
        return self.pes_nome

    class Meta:
        verbose_name = "Integrante"
        verbose_name_plural = "Integrantes"

class Cargo(models.Model):
    car_cod = models.AutoField(primary_key=True)
    car_descricao = models.CharField(max_length=255, verbose_name = "Cargo")
    car_ativo = models.BooleanField(default=True, verbose_name = "Ativo")

    def __str__(self):
        return self.car_descricao

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"

class AreaPesquisa(models.Model):
    ape_cod = models.AutoField(primary_key=True)
    ape_descricao = models.CharField(max_length=255, verbose_name = "Área de Pesquisa")
    def __str__(self):
        return self.ape_descricao

    class Meta:
        verbose_name = "Área de Pesquisa"
        verbose_name_plural = "Áreas de Pesquisa"

class Bolsista(models.Model):
    bol_cod = models.AutoField(primary_key=True)
    pes_cod = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name = "Integrante")
    bol_data_inicio = models.DateField(verbose_name = "Data de Ínicio da Bolsa")
    bol_data_fim = models.DateField(null=True, blank=True, verbose_name = "Data de Encerramento da Bolsa")
    ape_cod = models.ForeignKey(AreaPesquisa, on_delete=models.SET_NULL, null=True, verbose_name = "Área de Pesquisa")
    bol_tema = models.CharField(max_length=255, verbose_name = "Tema de Pesquisa", null=True, blank=True)
    cur_cod = models.ForeignKey(Curso, verbose_name= "Curso", on_delete=models.SET_NULL, null=True, blank=True)
    bol_ativo = models.BooleanField(default=True, verbose_name = "Ativo")

class MembroDiretoria(models.Model):
    dir_cod = models.AutoField(primary_key=True)
    pes_cod = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name = "Integrante")
    dir_data_inicio = models.DateField(verbose_name = "Data de Ínicio na Diretoria")
    dir_data_fim = models.DateField(null=True, blank=True, verbose_name = "Data de Encerramento na Diretoria")
    car_cod = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, verbose_name = "Cargo")
    dir_ativo = models.BooleanField(default=True, verbose_name = "Ativo")

    def __str__(self):
        return f"{self.pes_cod} - {self.car_cod}"

    class Meta:
        verbose_name = "Diretor(a)"
        verbose_name_plural = "Diretores"

class Oficio(models.Model):
    ofi_cod = models.AutoField(primary_key=True)
    ofi_destinatario = models.CharField(max_length=255, verbose_name = "Destinatário")
    ofi_assunto = models.CharField(max_length=255, verbose_name = "Assunto")
    ofi_numero = models.CharField(max_length=20, verbose_name = "Número do Ofício", unique=True, editable=True, null=True, blank=True)
    ofi_data = models.DateField(verbose_name = "Data do Ofício")
    ofi_texto = models.TextField(verbose_name = "Texto")
    dir_cod = models.ForeignKey(MembroDiretoria, on_delete=models.SET_NULL, null=True, verbose_name = "Diretor(a) Responsável pela Assinatura")

    def save(self, *args, **kwargs):
        if not self.ofi_numero:  
            ano_atual = self.ofi_data.year  
            ultimo_oficio = Oficio.objects.filter(ofi_numero__endswith=f'/{ano_atual}').order_by('-ofi_cod').first()
            if ultimo_oficio:
                ultimo_numero = int(ultimo_oficio.ofi_numero.split('/')[0])
                proximo_numero = ultimo_numero + 1
            else:
                proximo_numero = 1
            self.ofi_numero = f'{proximo_numero:02}/{ano_atual}'
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.ofi_numero} - {self.ofi_assunto}"

    class Meta:
        verbose_name = "Ofício"
        verbose_name_plural = "Ofícios"

class Evento(models.Model):
    eve_cod = models.AutoField(primary_key=True)
    eve_nome = models.CharField(max_length=255, verbose_name = "Nome do Evento")
    cid_local = models.ForeignKey(Cidade, null=True, on_delete=models.SET_NULL, verbose_name = "Cidade")
    est_cod = models.ForeignKey(Estado, null=True, on_delete=models.SET_NULL, verbose_name = "Estado")
    eve_data = models.DateField(verbose_name = "Data do Evento")
    eve_local_saida = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Local de Saída")
    eve_horario_saida = models.TimeField(null=True, blank=True, verbose_name = "Horário de Saída")
    eve_local_chegada = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Local de Chegada")
    eve_horario_chegada = models.TimeField(null=True, blank=True, verbose_name = "Horário de Chegada")
    eve_local_retorno = models.CharField(max_length=255, null=True, blank=True, verbose_name = "Local de Retorno")
    eve_horario_retorno = models.TimeField(null=True, blank=True, verbose_name = "Horário de Retorno")
    eve_data_retorno = models.DateField(null=True, blank=True, verbose_name = "Data do Retorno")
    Participantes = models.ManyToManyField(Pessoa, related_name="Participantes",null=True, blank=True)

    def clean(self):
        if self.eve_data < (datetime.strptime('01/01/2023', '%d/%m/%Y').date()):
            raise ValidationError({'eve_data': 'A data do evento não pode ser muito antiga.'})
        
        if (self.eve_data_retorno) and (self.eve_data_retorno < self.eve_data):
            raise ValidationError({'eve_data_retorno': 'A data de retorno não pode ser menor que a data do evento.'})
        
        if (self.eve_data_retorno) and (self.eve_data == self.eve_data_retorno):
            if self.eve_horario_retorno < self.eve_horario_saida:
                raise ValidationError({'eve_horario_retorno': 'A hora de retorno não pode ser menor que a hora de saída no mesmo dia.'})
        super().clean()

    def __str__(self):
        return self.eve_nome


class Agenda(models.Model):
    age_cod = models.AutoField(primary_key=True)
    age_titulo = models.CharField(max_length=100, verbose_name="Título")
    age_data = models.DateField(verbose_name = "Data do Evento/Compromisso")
    eve_cod = models.ForeignKey(Evento, on_delete=models.CASCADE, verbose_name = "Evento", null=True, blank=True)
    age_descricao = models.TextField(max_length=1000, verbose_name = "Descrição")

    
    
    def __str__(self):
        return f" {self.age_titulo}"

    class Meta:
        verbose_name = "Compromisso"
        verbose_name_plural = "Agenda"

class UsuarioPessoa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    pes_cod = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name="pessoa", db_column="pes_cod", null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Oficina(models.Model):
    ofc_cod = models.AutoField(primary_key=True)
    ofc_titulo = models.CharField(max_length=100, verbose_name="Título")
    ofc_ativo = models.BooleanField(default=True, verbose_name = "Ativo")
    
    def __str__(self):
        return self.ofc_titulo
    
class Oficineiro(models.Model):
    ofc_cod = models.AutoField(primary_key=True)
    pes_cod = models.ForeignKey(Pessoa, on_delete=models.CASCADE, null= True, verbose_name = "Integrante")
    Oficinas = models.ManyToManyField(Oficina, verbose_name = "Oficinas")
    ofc_ativo = models.BooleanField(default=True, verbose_name = "Ativo")

from django.db.models import Q

def get_pessoa_imagem(self):
    try:
        usuario_pessoa = UsuarioPessoa.objects.get(user=self)  # Corrige para 'user' em vez de 'usuario'
        return usuario_pessoa.pes_cod.pes_imagem.url if usuario_pessoa.pes_cod and usuario_pessoa.pes_cod.pes_imagem else None
    except UsuarioPessoa.DoesNotExist:
        return None

User.add_to_class('get_pessoa_imagem', get_pessoa_imagem)

