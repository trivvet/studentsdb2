# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-18 11:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentsdb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stprofile',
            name='extra_info',
        ),
    ]
