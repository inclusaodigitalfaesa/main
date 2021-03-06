# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-13 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pidfaesa', '0003_auto_20160913_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='CursoVoluntario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ds_nome', models.CharField(max_length=400, verbose_name='Curso')),
                ('is_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('dthr_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criacao')),
            ],
        ),
        migrations.CreateModel(
            name='EscolaVoluntario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ds_nome', models.CharField(max_length=400, verbose_name='Escola')),
                ('is_ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('dthr_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criacao')),
            ],
        ),
        migrations.CreateModel(
            name='Voluntario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ds_nome', models.CharField(max_length=400, verbose_name='Nome')),
                ('ds_email', models.EmailField(max_length=200, verbose_name='Email')),
                ('ds_telefone', models.CharField(max_length=30, verbose_name='Telefone')),
                ('dthr_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criacao')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.CursoVoluntario')),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.EscolaVoluntario')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.Turma')),
            ],
        ),
        migrations.AlterField(
            model_name='aluno',
            name='ds_email',
            field=models.EmailField(blank=True, max_length=200, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='dthr_criacao',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data de criacao'),
        ),
    ]
