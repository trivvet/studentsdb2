# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from datetime import date

class MonthJournal(models.Model):
    """Journal Model"""

    class Meta(object):
        verbose_name=u"Місячний Журнал"
        verbose_name_plural=u"Місячні Журнали"

    student_name = models.ForeignKey('Student',
        verbose_name=u"Студент",
        blank=False,
        unique_for_month='date')

    date = models.DateField(
        verbose_name=u"Дата",
        blank=False)

    for day in range(1,32):
        exec('present_day%s = models.BooleanField(default=False)' % day)
    
    def __unicode__(self):
        return u"%s: %d %d" % (self.student_name.last_name, self.date.month,
            self.date.year)

    
