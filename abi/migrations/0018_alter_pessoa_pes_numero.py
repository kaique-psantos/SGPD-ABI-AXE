# Generated by Django 5.1.1 on 2024-11-26 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abi', '0017_alter_agenda_age_titulo_alter_pessoa_pes_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='pes_numero',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Número'),
        ),
    ]
