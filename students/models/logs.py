# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

from django.db import models

class LogEntry(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name=u"Подія"
        verbose_name_plural=u"Події"

    log_datetime = models.DateTimeField(
        verbose_name=u"Дата та час",
        blank=False)

    status = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Статус")

    signal = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва сигналу")   
   
    info = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Текст сигналу")

    def __unicode__(self):
        return u"%s %s (%s)" % (self.status, self.signal, datetime.strftime(self.log_datetime, '%Y-%m-%d %H:%M:%S'))
