# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 23:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pidfaesa', '0009_auto_20160918_1912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alun_Resp_Perg_Ques',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dthr_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data de criacao')),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.Aluno')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.Pergunta')),
                ('questionario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.Questionario')),
                ('resposta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pidfaesa.Resposta')),
            ],
        ),
    ]
