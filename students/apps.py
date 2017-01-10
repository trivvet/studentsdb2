# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.apps import AppConfig
from django.dispatch import Signal
from django.db.models.signals import post_migrate
  

class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = u'База даних студентів'

    def ready(self):
        from students import signals
        post_migrate.connect(signals.log_migrate_dote, sender=self)
