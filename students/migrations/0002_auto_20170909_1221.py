# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-09 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='time_change',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Time of last modification'),
        ),
    ]
