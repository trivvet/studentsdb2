# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-02 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stud_auth', '0002_stprofile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='stprofile',
            name='language',
            field=models.CharField(blank=True, max_length=10, verbose_name='Language'),
        ),
        migrations.AddField(
            model_name='stprofile',
            name='time_zone',
            field=models.CharField(blank=True, max_length=128, verbose_name='\u0427\u0430\u0441\u043e\u0432\u0430 \u0437\u043e\u043d\u0430'),
        ),
    ]
