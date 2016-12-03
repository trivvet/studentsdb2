# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 16:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(verbose_name='\u041e\u0446\u0456\u043d\u043a\u0430')),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u0456\u0441\u043f\u0438\u0442\u0443',
                'verbose_name_plural': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u0456\u0441\u043f\u0438\u0442\u0456\u0432',
            },
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Group', verbose_name='\u0413\u0440\u0443\u043f\u0430'),
        ),
        migrations.AddField(
            model_name='result',
            name='result_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='students.Exam', verbose_name='\u041f\u0440\u0435\u0434\u043c\u0435\u0442'),
        ),
        migrations.AddField(
            model_name='result',
            name='result_student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442'),
        ),
    ]