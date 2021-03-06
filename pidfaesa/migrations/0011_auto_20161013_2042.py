# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 23:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pidfaesa', '0010_alun_resp_perg_ques'),
    ]

    operations = [
        migrations.CreateModel(
            name='PresencaAluno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dt_presenca', models.DateField(verbose_name='Data da prsenca')),
                ('no_hora_aula', models.PositiveSmallIntegerField(verbose_name='Hora aula')),
                ('dthr_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criacao')),
            ],
        ),
        migrations.AddField(
            model_name='aluno',
            name='no_hora_aula_total',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Hora aula total'),
        ),
        migrations.AddField(
            model_name='voluntario',
            name='no_hora_aula_total',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Hora aula total'),
        ),
        migrations.AddField(
            model_name='presencaaluno',
            name='aluno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.Aluno'),
        ),
    ]
