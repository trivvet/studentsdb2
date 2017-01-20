# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from datetime import date

from django.db import models
from django.utils.translation import ugettext_lazy as _

class MonthJournal(models.Model):
    """Journal Model"""

    class Meta(object):
        verbose_name=_(u"Month Journal")
        verbose_name_plural=_(u"Month Journals")

    student_name = models.ForeignKey('Student',
        verbose_name=_(u"Student"),
        blank=False,
        unique_for_month='date')

    date = models.DateField(
        verbose_name=_(u"Date"),
        blank=False)

    for day in range(1,32):
        exec('present_day%s = models.BooleanField(default=False)' % day)
    
    def __unicode__(self):
        return u"%s: %d %d" % (self.student_name.last_name, self.date.month,
            self.date.year)

    
