from __future__ import unicode_literals

from django.apps import AppConfig
from django.dispatch import Signal
from django.db.models.signals import post_migrate
from django.utils.translation import ugettext_lazy as _ 

class StudentsAppConfig(AppConfig):
    name = 'students'
    verbose_name = _(u'Students Accounting Service')

    def ready(self):
        from students import signals
        post_migrate.connect(signals.log_migrate_dote, sender=self)
