# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-18 19:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pidfaesa', '0006_remove_turma_ds_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='turma',
            name='hr_fim',
            field=models.TimeField(default=datetime.time(12, 0), verbose_name='Hora de fim'),
        ),
        migrations.AddField(
            model_name='turma',
            name='hr_ini',
            field=models.TimeField(default=datetime.time(8, 0), verbose_name='Hora de inicio'),
        ),
    ]
