# Generated by Django 5.1.1 on 2024-12-02 17:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abi', '0004_pessoa_cid_cod_pessoa_end_bairro_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oficineiro',
            name='pes_cod',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='abi.pessoa', verbose_name='Integrante'),
        ),
    ]
