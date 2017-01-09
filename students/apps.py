# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.dispatch import Signal
  

class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = u'База даних студентів'

    def ready(self):
        from students import signals
