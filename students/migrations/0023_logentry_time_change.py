# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-07 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0022_auto_20170902_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='time_change',
            field=models.DateTimeField(auto_now=True, verbose_name='\u0427\u0430\u0441 \u043e\u0441\u0442\u0430\u043d\u043d\u044c\u043e\u0457 \u043c\u043e\u0434\u0438\u0444\u0456\u043a\u0430\u0446\u0456\u0457'),
        ),
    ]
