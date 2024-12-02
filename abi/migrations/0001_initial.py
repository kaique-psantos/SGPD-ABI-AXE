# Generated by Django 5.1.1 on 2024-12-02 23:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaArtistica',
            fields=[
                ('are_cod', models.AutoField(primary_key=True, serialize=False)),
                ('are_descricao', models.CharField(max_length=255, verbose_name='Campo Artistico')),
                ('are_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'verbose_name': 'Campo Artistico',
                'verbose_name_plural': 'Campo Artistico',
            },
        ),
        migrations.CreateModel(
            name='AreaPesquisa',
            fields=[
                ('ape_cod', models.AutoField(primary_key=True, serialize=False)),
                ('ape_descricao', models.CharField(max_length=255, verbose_name='Área de Pesquisa')),
            ],
            options={
                'verbose_name': 'Área de Pesquisa',
                'verbose_name_plural': 'Áreas de Pesquisa',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('car_cod', models.AutoField(primary_key=True, serialize=False)),
                ('car_descricao', models.CharField(max_length=255, verbose_name='Cargo')),
                ('car_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
            },
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('cid_cod', models.AutoField(primary_key=True, serialize=False)),
                ('cid_descricao', models.CharField(max_length=255, verbose_name='Cidade')),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
            },
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('cur_cod', models.AutoField(primary_key=True, serialize=False)),
                ('cur_descricao', models.CharField(max_length=255, verbose_name='Curso')),
                ('cur_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
        ),
        migrations.CreateModel(
            name='Escolaridade',
            fields=[
                ('esc_cod', models.AutoField(primary_key=True, serialize=False)),
                ('esc_descricao', models.CharField(max_length=255, verbose_name='Escolaridade')),
            ],
            options={
                'verbose_name': 'Escolaridade',
                'verbose_name_plural': 'Escolaridades',
            },
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('est_cod', models.AutoField(primary_key=True, serialize=False)),
                ('est_descricao', models.CharField(max_length=100, verbose_name='Estado')),
                ('est_sigla', models.CharField(max_length=2, verbose_name='Sigla do Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Etnia',
            fields=[
                ('etn_cod', models.AutoField(primary_key=True, serialize=False)),
                ('etn_descricao', models.CharField(max_length=255, verbose_name='Etnia/Raça')),
            ],
            options={
                'verbose_name': 'Etnia/Raça',
                'verbose_name_plural': 'Etnias/Raças',
            },
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('gen_cod', models.AutoField(primary_key=True, serialize=False)),
                ('gen_descricao', models.CharField(max_length=255, verbose_name='Gênero')),
            ],
            options={
                'verbose_name': 'Gênero',
                'verbose_name_plural': 'Gêneros',
            },
        ),
        migrations.CreateModel(
            name='OrientacaoSexual',
            fields=[
                ('ori_cod', models.AutoField(primary_key=True, serialize=False)),
                ('ori_descricao', models.CharField(max_length=255, verbose_name='Orientação Sexual')),
            ],
            options={
                'verbose_name': 'Orientação Sexual',
                'verbose_name_plural': 'Orientações Sexuais',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('pai_cod', models.AutoField(primary_key=True, serialize=False)),
                ('pai_sigla', models.CharField(max_length=2, verbose_name='Sigla do País')),
                ('pai_descricao', models.CharField(max_length=100, verbose_name='País')),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('end_cod', models.AutoField(primary_key=True, serialize=False)),
                ('end_rua', models.CharField(blank=True, max_length=255, null=True, verbose_name='Rua')),
                ('end_bairro', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bairro')),
                ('end_numero', models.CharField(blank=True, max_length=10, null=True, verbose_name='Numero')),
                ('end_complemento', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('end_referencia', models.CharField(blank=True, max_length=255, null=True, verbose_name='Referência')),
                ('cid_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abi.cidade', verbose_name='Cidade')),
                ('est_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abi.estado', verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Endereço',
                'verbose_name_plural': 'Endereços',
            },
        ),
        migrations.AddField(
            model_name='cidade',
            name='est_cod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abi.estado', verbose_name='Estado'),
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('eve_cod', models.AutoField(primary_key=True, serialize=False)),
                ('eve_nome', models.CharField(max_length=255, verbose_name='Nome do Evento')),
                ('eve_data', models.DateField(verbose_name='Data do Evento')),
                ('eve_local_saida', models.CharField(blank=True, max_length=255, null=True, verbose_name='Local de Saída')),
                ('eve_horario_saida', models.TimeField(blank=True, null=True, verbose_name='Horário de Saída')),
                ('eve_local_chegada', models.CharField(blank=True, max_length=255, null=True, verbose_name='Local de Chegada')),
                ('eve_horario_chegada', models.TimeField(blank=True, null=True, verbose_name='Horário de Chegada')),
                ('eve_local_retorno', models.CharField(blank=True, max_length=255, null=True, verbose_name='Local de Retorno')),
                ('eve_horario_retorno', models.TimeField(blank=True, null=True, verbose_name='Horário de Retorno')),
                ('eve_data_retorno', models.DateField(blank=True, null=True, verbose_name='Data do Retorno')),
                ('cid_local', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.cidade', verbose_name='Cidade')),
                ('est_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.estado', verbose_name='Estado')),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('age_cod', models.AutoField(primary_key=True, serialize=False)),
                ('age_descricao', models.TextField(max_length=255, verbose_name='Descrição')),
                ('age_data', models.DateField(verbose_name='Data do Evento/Compromisso')),
                ('eve_cod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='abi.evento', verbose_name='Evento')),
            ],
            options={
                'verbose_name': 'Compromisso',
                'verbose_name_plural': 'Agenda',
            },
        ),
        migrations.CreateModel(
            name='MembroDiretoria',
            fields=[
                ('dir_cod', models.AutoField(primary_key=True, serialize=False)),
                ('dir_data_inicio', models.DateField(verbose_name='Data de Ínicio na Diretoria')),
                ('dir_data_fim', models.DateField(blank=True, null=True, verbose_name='Data de Encerramento na Diretoria')),
                ('dir_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('car_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.cargo', verbose_name='Cargo')),
            ],
            options={
                'verbose_name': 'Diretor(a)',
                'verbose_name_plural': 'Diretores',
            },
        ),
        migrations.CreateModel(
            name='Oficio',
            fields=[
                ('ofi_cod', models.AutoField(primary_key=True, serialize=False)),
                ('ofi_destinatario', models.CharField(max_length=255, verbose_name='Destinatário')),
                ('ofi_assunto', models.CharField(max_length=255, verbose_name='Assunto')),
                ('ofi_numero', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Número do Ofício')),
                ('ofi_data', models.DateField(verbose_name='Data do Ofício')),
                ('ofi_texto', models.TextField(verbose_name='Texto')),
                ('dir_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.membrodiretoria', verbose_name='Diretor(a) Responsável pela Assinatura')),
            ],
            options={
                'verbose_name': 'Ofício',
                'verbose_name_plural': 'Ofícios',
            },
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('pes_cod', models.AutoField(primary_key=True, serialize=False)),
                ('pes_nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('pes_data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('pes_cpf', models.CharField(max_length=11, verbose_name='CPF')),
                ('pes_email', models.CharField(max_length=255, verbose_name='E-mail')),
                ('pes_telefone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('pes_celular', models.CharField(max_length=15, verbose_name='Celular')),
                ('pes_data_ingresso', models.DateField(verbose_name='Data de Ingresso')),
                ('pes_data_saida', models.DateField(blank=True, null=True, verbose_name='Data de Saída')),
                ('pes_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('pes_imagem', models.ImageField(blank=True, null=True, upload_to='imagens/', verbose_name='Imagem')),
                ('end_rua', models.CharField(blank=True, max_length=255, null=True, verbose_name='Rua')),
                ('end_bairro', models.CharField(blank=True, max_length=255, null=True, verbose_name='Bairro')),
                ('end_numero', models.CharField(blank=True, max_length=10, null=True, verbose_name='Número')),
                ('end_complemento', models.CharField(blank=True, max_length=255, null=True, verbose_name='Complemento')),
                ('end_referencia', models.CharField(blank=True, max_length=255, null=True, verbose_name='Referência')),
                ('are_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.areaartistica', verbose_name='Área Artistica')),
                ('cid_cod', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='abi.cidade', verbose_name='Cidade')),
                ('cid_naturalidade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='naturalidade', to='abi.cidade', verbose_name='Cidade')),
                ('end_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.endereco', verbose_name='Endereço')),
                ('esc_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.escolaridade', verbose_name='Escolaridade')),
                ('est_cod', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='abi.estado', verbose_name='Estado')),
                ('est_naturalidade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='naturalidade', to='abi.estado', verbose_name='Estado')),
                ('etn_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.etnia', verbose_name='Etnia')),
                ('gen_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.genero', verbose_name='Gênero')),
                ('ori_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.orientacaosexual', verbose_name='Orientação Sexual')),
            ],
            options={
                'verbose_name': 'Integrante',
                'verbose_name_plural': 'Integrantes',
            },
        ),
        migrations.CreateModel(
            name='Oficineiro',
            fields=[
                ('ofc_cod', models.AutoField(primary_key=True, serialize=False)),
                ('ofc_descricao', models.CharField(max_length=255, verbose_name='Nome da Oficina')),
                ('ofc_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('pes_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='abi.pessoa', verbose_name='Integrante')),
            ],
        ),
        migrations.AddField(
            model_name='membrodiretoria',
            name='pes_cod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abi.pessoa', verbose_name='Integrante'),
        ),
        migrations.CreateModel(
            name='Bolsista',
            fields=[
                ('bol_cod', models.AutoField(primary_key=True, serialize=False)),
                ('bol_data_inicio', models.DateField(verbose_name='Data de Ínicio da Bolsa')),
                ('bol_data_fim', models.DateField(blank=True, null=True, verbose_name='Data de Encerramento da Bolsa')),
                ('bol_tema', models.CharField(blank=True, max_length=255, null=True, verbose_name='Tema de Pesquisa')),
                ('bol_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('ape_cod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.areapesquisa', verbose_name='Área de Pesquisa')),
                ('cur_cod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='abi.curso', verbose_name='Curso')),
                ('pes_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abi.pessoa', verbose_name='Integrante')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioPessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pes_cod', models.ForeignKey(blank=True, db_column='pes_cod', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pessoa', to='abi.pessoa')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventoXPessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eve_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abi.evento')),
                ('pes_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abi.pessoa')),
            ],
            options={
                'verbose_name': 'Integrante no Evento',
                'verbose_name_plural': 'Integrantes no Evento',
                'unique_together': {('eve_cod', 'pes_cod')},
            },
        ),
    ]
