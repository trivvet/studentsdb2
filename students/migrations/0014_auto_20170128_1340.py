# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-28 13:40
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('students', '0013_auto_20170112_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('language', models.CharField(max_length=10, verbose_name='Language')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'verbose_name': 'Exam', 'verbose_name_plural': 'Exams'},
        ),
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Group', 'verbose_name_plural': 'Groups'},
        ),
        migrations.AlterModelOptions(
            name='monthjournal',
            options={'verbose_name': 'Month Journal', 'verbose_name_plural': 'Month Journals'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name': 'Exam results', 'verbose_name_plural': 'Exams results'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
        migrations.AlterField(
            model_name='exam',
            name='date',
            field=models.DateTimeField(null=True, verbose_name='Data and time of event'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='exam_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Group', verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Additional notes'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='teacher_name',
            field=models.CharField(max_length=256, verbose_name='Lecturer'),
        ),
        migrations.AlterField(
            model_name='group',
            name='leader',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='students.Student', verbose_name='Leader'),
        ),
        migrations.AlterField(
            model_name='group',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Additional notes'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=256, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='monthjournal',
            name='student_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student', unique_for_month='date', verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_exam',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='students.Exam', verbose_name='Subject'),
        ),
        migrations.AlterField(
            model_name='result',
            name='result_student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Student', verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='result',
            name='score',
            field=models.IntegerField(verbose_name='Mark'),
        ),
        migrations.AlterField(
            model_name='student',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=256, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=256, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='middle_name',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Additional notes'),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=b'', verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='students.Group', verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='student',
            name='ticket',
            field=models.IntegerField(unique=True, verbose_name='Ticket'),
        ),
    ]