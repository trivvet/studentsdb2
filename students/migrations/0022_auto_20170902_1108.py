# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-09-02 11:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0021_auto_20170902_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='logentry_requests_created', to=settings.AUTH_USER_MODEL, verbose_name='User who created'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='logentry_requests_modified', to=settings.AUTH_USER_MODEL, verbose_name='User who modified'),
        ),
    ]
