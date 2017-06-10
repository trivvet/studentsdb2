from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _

class LogEntry(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name=_(u"Event")
        verbose_name_plural=_(u"Events")

    log_datetime = models.DateTimeField(
        verbose_name=_(u"Date and time"),
        blank=False)

    status = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Status"))

    signal = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Signal name"))   
   
    info = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Signal text"))

    def __unicode__(self):
        return u"%s %s (%s)" % (self.status, self.signal, datetime.strftime(self.log_datetime, '%Y-%m-%d %H:%M:%S'))
